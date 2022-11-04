import struct, time
import logger

UART_READ_SIZE = 128 #64, 128, 256

THROTTLE_SERVO = 1  
YAW_SERVO = 2
UP_SERVO = 3
MSG_RATE = 50000 #20Hz messaging rate
MSG_RATE_LIDAR = 50000
RCCH = 35
ATTITUDE = 30
SERVO = 36
LIDAR = 132

SUPPRESS_MSG = -1



class MavLink():
    '''Implements select Mavlink v1 messages to enable bydirectional communication between 
    OpenMV and Pixracer (ardupilot)'''
    def __init__(self,hw):
        self.hw = hw
        self._uart = hw.uart
        self.__ps = -1 #starting packet number
        self.ser_buf = bytearray()

        time.sleep(0.25) #Allow UART to initialize before sending messages MAYBE NOT NEEDED

        reject_msg = [74,65,1,42,227,77,22,253,125,27,24,241,0,146,2,165,163,168,233,116,172,193]
        for msg in reject_msg:
            self.send_set_msg_interval_cmd(msg,SUPPRESS_MSG)

        self.send_set_msg_interval_cmd(RCCH,MSG_RATE) #RC_Channels_Raw
        self.send_set_msg_interval_cmd(ATTITUDE,MSG_RATE) #Attitude
        self.send_set_msg_interval_cmd(SERVO,MSG_RATE) #Servo Channels
        self.send_set_msg_interval_cmd(LIDAR,MSG_RATE) #LIDAR

        self.send_set_msg_interval_cmd(RCCH,MSG_RATE) #RC_Channels_Raw
        self.send_set_msg_interval_cmd(ATTITUDE,MSG_RATE) #Attitude
        self.send_set_msg_interval_cmd(SERVO,MSG_RATE) #Servo Channels
        self.send_set_msg_interval_cmd(LIDAR,MSG_RATE_LIDAR) #LIDAR


    def __get_ps(self):
        '''update packet sequence number'''
        self.__ps += 1
        if self.__ps > 255:
            self.__ps = 0

        return self.__ps


    def __checksum(self,data, extra):
        '''Calculate checksum of packet
        https://github.com/mavlink/c_library_v1/blob/master/checksum.h'''
        output = 0xFFFF
        for i in range(len(data)):
            tmp = data[i] ^ (output & 0xFF)
            tmp = (tmp ^ (tmp << 4)) & 0xFF
            output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
        tmp = extra ^ (output & 0xFF)
        tmp = (tmp ^ (tmp << 4)) & 0xFF
        output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
        return output


    def __msg_frame(self,msg_id, extra_crc, payload, ps, sys_id=1, comp_id=1):
        '''builds serial mavlink packet with checksum'''
        payload_len = len(payload)
        msg = struct.pack("<BBBBB{}s".format(payload_len), #https://mavlink.io/en/guide/serialization.html#v1_packet_format
                            payload_len,
                            ps & 0xFF,
                            sys_id,
                            comp_id,
                            msg_id,
                            payload)

        return struct.pack("<B{}sH".format(5+payload_len),
                            0xFE,
                            msg,
                            self.__checksum(msg,extra_crc))


    def _build_msg_param_req_lst(self):
        '''Requests a list of all the available parameters and their current values
        https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_param_request_list.h'''
        system_id = 1 #1 is main flight controller
        component_id = 1 #not sure what "1" is, but hopefully it is the main component of the flight controller
        payload = struct.pack("<bb",system_id,component_id) #payload format from https://mavlink.io/en/messages/common.html#PARAM_REQUEST_LIST
  
        return self.__msg_frame(21,159,payload,self.__get_ps())


    def _build_msg_manual_control(self, x=0, #pitch (fwd/bk of right stick)
                                          y=0, #roll (left/right of right stick)
                                          z=0, #thrust (fwd/bk of left stick)
                                          r=0, #yaw (left/right of left stick)
                                          buttons=0): #8-bit bitfield
        '''NOTE: CURRENTLY NOTE IMPELEMENTED
        https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_manual_control.h'''
        target = 0 #target system to be controlled #TODO what does this mean?
        payload = struct.pack("<hhhhHB",x,y,z,r,buttons,target) 
     
        return self.__msg_frame(69,243,payload,self.__get_ps())



    def _build_msg_ch_overide(self, ch=(0,0,0,0,0,0,0,0)):
        '''NOTE: CURRENTLY NOTE IMPELEMENTED
        https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_rc_channels_override.h'''
        target_system = 1
        target_component = 1
        payload = struct.pack("<8HBB",ch[0],ch[1],ch[2],ch[3],ch[4],ch[5],ch[6],ch[7],
                                target_system,target_component)
 
        return self.__msg_frame(70,124,payload,self.__get_ps())


    def _build_msg_cmd_long(self,cmd,params=[float('NaN')]*7):
        '''Command Protocol message, mavlink returns Command ACK (#77) upon receipt of this message
        https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_command_long.h'''
        if len(params)<7:
            logger.log.verbose("ERROR: command_long message requires exactly 7 parameters, unused param locations should be filled with NaN.")
            return False
        target_system = 1
        target_component = 1 #TODO maybe "0"?
        confirm = 0 #TODO nonzero for retransmits
        payload = struct.pack("<7fHBBB",params[0],params[1],params[2],params[3],
                                        params[4],params[5],params[6],
                                        cmd,target_system,target_component,confirm)

        return self.__msg_frame(76,152,payload,self.__get_ps())


    def _build_msg_set_msg_int(self,msg_id,interval,target=0):
        '''Set params for mav_cmd_set_message_interval #511
        id = message number
        inter = interval in usec'''
        return [msg_id,interval,float('Nan'),float('NaN'),float('NaN'),float('NaN'),target]


    def _build_msg_cmd_req_msg(self,id):
        '''Functions similar to _build_msg_set_msg_int, but used for ONE SHOT messages
        Set params for mav_cmd_request_message #512'''
        return [id,float('Nan'),float('NaN'),float('NaN'),float('NaN'),float('NaN'),float('NaN')]


    def _build_frame_cmd_do_set_servo(self,servo_ch,value):
        '''Set params for mav_cmd_do_set_servo #183
        servo_ch= servo channel number
        value = PWM value (us)
        '''
        return [servo_ch,value,float('NaN'),float('NaN'),float('NaN'),float('NaN'),float('NaN')]

    def _build_frame_cmd_do_repeat_servo(self,servo_ch,value):
        '''Set params for mav_cmd_do_repeat_servo #184
        servo_ch= servo channel number
        value = PWM value (us)
        cycle_count = count
        cycle_time = time_in_seconds (some discussion that maybe this is really in ms)
        '''
        return [servo_ch,value,1,0.5,float('NaN'),float('NaN'),float('NaN')]


    def send_set_msg_interval_cmd(self,msg_id,interval):
        '''Send cmd message #511 to set desired publish rate of msg.
        msg_id = message type to be published
        interval = message interval in us'''
        cmd = self._build_msg_cmd_long(511,params=self._build_msg_set_msg_int(msg_id,interval,target=0))
        self._uart.write(cmd)


    def send_set_servo_cmd(self,servo,pwm):
        '''Send command messsage to set values of individual servos'''
        cmd = self._build_msg_cmd_long(183,params=self._build_frame_cmd_do_set_servo(servo,pwm))
        #cmd = self._build_msg_cmd_long(184,params=self._build_frame_cmd_do_repeat_servo(servo,pwm))
        self._uart.write(cmd)
        logger.log.verbose('Sent motor command -- SERVO:' + str(servo) + ' PWM: ' + str(pwm))


    def __cntl_to_pwm(self,value):
        '''Helper to convert -1 -- 1 values of controls to PWM values (us)'''
        return(400*value+1500)


    def setControls(self,controls):
        '''Send corresponding mavlink message to set servo values based on current settings of controls object'''

        self.send_set_servo_cmd(YAW_SERVO,self.__cntl_to_pwm(controls.yaw)) #YAW Servo Channel 2
        self.send_set_servo_cmd(THROTTLE_SERVO,self.__cntl_to_pwm(controls.throttle)) #THROTTLE Servo Channel 1
        self.send_set_servo_cmd(UP_SERVO,self.__cntl_to_pwm(controls.up)) #UP Servo Channel 3


    def _read_uart(self): #TODO Run tests to see if buffer is emptying out fast enough
        '''Read contents of serial buffer and parse messages
        Parse a message:
            msg[0] = start byte (254)
            msg[1] = message payload length (not including header or checksum
            msg[2] = sequence number (0-255)
            msg[3] = systems id (should always be 1)
            msg[4] = component id (usually 1)
            msg[5] = message type 
            msg[6:6+n] = payload n = message payload length
            msg[6+n:6+n+3] = checksum'''
        #logger.log.verbose('bytes in uart: ' + str(self._uart.any()))
        result = self._uart.read(UART_READ_SIZE)
       
        if result == None:
            return None
        else:
            r_pntr = 0 #read_pointer - tracks read position in message buffer
            msg_list = [] #stores all parsed messages
            while r_pntr < len(result):
                if result[r_pntr] == 254:
                    try: #Message found
                        msg_type = result[r_pntr+5] #Message Id
                        payload = result[r_pntr+6:r_pntr+6+result[r_pntr+1]] #Msg payload in bytes
                        msg = (result[r_pntr+5],payload)
                        msg_list.append(msg)
                        r_pntr += 6+result[r_pntr+1]+2 #advance read pointer to next message
                    except IndexError:
                        #Incomplete Message
                        r_pntr += 1
                else:
                    r_pntr += 1
            return msg_list


    def __parse_lidar_msg(self,msg):
        '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_distance_sensor.h
           https://mavlink.io/en/messages/common.html#DISTANCE_SENSOR
           Byte order:
            char buf[MAVLINK_MSG_ID_DISTANCE_SENSOR_LEN];
            _mav_put_uint32_t(buf, 0, time_boot_ms);
            _mav_put_uint16_t(buf, 4, min_distance);
            _mav_put_uint16_t(buf, 6, max_distance);
            _mav_put_uint16_t(buf, 8, current_distance);
            _mav_put_uint8_t(buf, 10, type);
            _mav_put_uint8_t(buf, 11, id);
            _mav_put_uint8_t(buf, 12, orientation);
            _mav_put_uint8_t(buf, 13, covariance);
        '''
        try:
            return struct.unpack('<1H',msg[8:10])[0] #current_distance
  
        except ValueError:
            return None


    def __parse_attitude_msg(self,msg):
        '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_attitude.h
           https://mavlink.io/en/messages/common.html#ATTITUDE
           Byte order: 
            char buf[MAVLINK_MSG_ID_ATTITUDE_LEN];
            _mav_put_uint32_t(buf, 0, time_boot_ms);
            _mav_put_float(buf, 4, roll);
            _mav_put_float(buf, 8, pitch);
            _mav_put_float(buf, 12, yaw);
            _mav_put_float(buf, 16, rollspeed);
            _mav_put_float(buf, 20, pitchspeed);
            _mav_put_float(buf, 24, yawspeed);
        '''
        try:
            att_tup = struct.unpack('<6f',msg[4:28]) #(roll,pitch,yaw,rollspeed,pitchspeed,yawspeed)
            return {'roll': att_tup[0],'pitch':att_tup[1],'yaw':att_tup[2],
                    'roll_speed':att_tup[3],'pitch_speed':att_tup[4],'yaw_speed':att_tup[5]}
            #return (struct.unpack('<6f',msg[4:28])) 
        except ValueError:
            return None


    def __parse_rc_ch_msg(self,msg):
        '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_rc_channels_raw.h
           https://mavlink.io/en/messages/common.html#RC_CHANNELS_RAW
           Byte Order:
            char buf[MAVLINK_MSG_ID_RC_CHANNELS_RAW_LEN];
            _mav_put_uint32_t(buf, 0, time_boot_ms);
            _mav_put_uint16_t(buf, 4, chan1_raw);
            _mav_put_uint16_t(buf, 6, chan2_raw);
            _mav_put_uint16_t(buf, 8, chan3_raw);
            _mav_put_uint16_t(buf, 10, chan4_raw);
            _mav_put_uint16_t(buf, 12, chan5_raw);
            _mav_put_uint16_t(buf, 14, chan6_raw);
            _mav_put_uint16_t(buf, 16, chan7_raw);
            _mav_put_uint16_t(buf, 18, chan8_raw);
            _mav_put_uint8_t(buf, 20, port);
            _mav_put_uint8_t(buf, 21, rssi);
        '''
        try:
            rc_tup = struct.unpack('<8H',msg[4:20]) #(roll,pitch,yaw,rollspeed,pitchspeed,yawspeed)
            return {'ch1': rc_tup[0],'ch2':rc_tup[1],'ch3':rc_tup[2],
                    'ch4':rc_tup[3],'ch5':rc_tup[4],'ch6':rc_tup[5],
                    'ch7':rc_tup[6],'ch8':rc_tup[7]}
            #return (struct.unpack('<8H',msg[4:20]))
        except ValueError:
            return None


    def __parse_servo_output_msg(self,msg):
        '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_servo_output_raw.h
           https://mavlink.io/en/messages/common.html#SERVO_OUTPUT_RAW
           Byte order:
            _mav_put_uint32_t(buf, 0, time_usec);
            _mav_put_uint16_t(buf, 4, servo1_raw);
            _mav_put_uint16_t(buf, 6, servo2_raw);
            _mav_put_uint16_t(buf, 8, servo3_raw);
            _mav_put_uint16_t(buf, 10, servo4_raw);
            _mav_put_uint16_t(buf, 12, servo5_raw);
            _mav_put_uint16_t(buf, 14, servo6_raw);
            _mav_put_uint16_t(buf, 16, servo7_raw);
            _mav_put_uint16_t(buf, 18, servo8_raw);
            _mav_put_uint8_t(buf, 20, port);'''
        try:
            sv_tup = struct.unpack('<8H',msg[4:20])
            return {'servo1': sv_tup[0],'servo2':sv_tup[1],'servo3':sv_tup[2],
                    'servo4':sv_tup[3],'servo5':sv_tup[4],'servo6':sv_tup[5],
                    'servo7':sv_tup[6],'servo8':sv_tup[7]}
        except ValueError:
            return None


    def getSensors(self):
        '''Returns dict where key = Sensor_type, value = most recent value received via mavlink'''
        start = time.time_ns()
        msg_list = self._read_uart()     
        uartReadTime = (time.time_ns() - start)/1e9
        logger.log.verbose('mavlink uart read: ' + str(uartReadTime))
        


        if(msg_list == None):
            logger.log.warning(">>>>>>>>>>>>>>>>>>") 
            logger.log.warning("MAVLINK LINK FAIL")
            logger.log.warning(">>>>>>>>>>>>>>>>>>") 
            self.hw.systemFail()

        sensors = {'Attitude': None, 'RCCH': None, 'Servo': None, 'Lidar': None}
        
        if msg_list != None:
            for msg in msg_list:
                if msg[0] == ATTITUDE:
                    result = self.__parse_attitude_msg(msg[1])
                    if result != None:
                        sensors['Attitude'] = result
                        logger.log.info("mavlink 1 - new attitude data!")
                elif msg[0] == RCCH:
                    result = self.__parse_rc_ch_msg(msg[1])
                    if result != None:
                        sensors['RCCH'] = result
                        logger.log.info("mavlink 2 - new rcch data!")
                elif msg[0] == SERVO:
                    result = self.__parse_servo_output_msg(msg[1])
                    if result != None:
                        sensors['Servo'] = result
                        logger.log.info("mavlink 3 - new servo data!")
                elif msg[0] == LIDAR:
                    result = self.__parse_lidar_msg(msg[1])  
                   # logger.log.verbose('^^^^^^^^LIDAR^^^^^^^^^^^^^^^^')  
                    #logger.log.verbose(result)
                    #logger.log.debugOnly('lidar value = ' + str(result))                    
                   # logger.log.verbose('^^^^^^^^^^^^^^^^^^^^^^^^')               
                    if result != None:                                               
                        sensors['Lidar'] = result
                        logger.log.info("mavlink 4 - new lidar data!")

        return sensors #Any sensor that is not updated will return 'None'


if __name__ == "__main__":
    mvlink = MavLink(hw)
    result = mvlink.getSensors()
    logger.log.verbose(result)
