import pyb, struct, time

THROTTLE_SERVO = 1
YAW_SERVO = 2
UP_SERVO = 3
MSG_RATE = 200000 #5Hz messaging rate


class MavLink():
    '''Implements select Mavlink v1 messages to enable bydirectional communication between 
    OpenMV and Pixracer (ardupilot)'''
    def __init__(self,uart=3,baudrate=115200):
        self._uart = pyb.UART(uart,baudrate,timeout_char=1000)
        self.__ps = -1 #starting packet number
        self.ser_buf = bytearray()

        time.sleep(0.25) #Allow UART to initialize before sending messages MAYBE NOT NEEDED

        self.send_set_msg_interval_cmd(35,MSG_RATE) #RC_Channels_Raw
        self.send_set_msg_interval_cmd(30,MSG_RATE) #Attitude
        self.send_set_msg_interval_cmd(36,MSG_RATE) #Servo Channels
        self.send_set_msg_interval_cmd(132,MSG_RATE) #LIDAR


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
            print("ERROR: command_long message requires exactly 7 parameters, unused param locations should be filled with NaN.")
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


    def send_set_msg_interval_cmd(self,msg_id,interval):
        '''Send cmd message #511 to set desired publish rate of msg.
        msg_id = message type to be published
        interval = message interval in us'''
        cmd = self._build_msg_cmd_long(511,params=self._build_msg_set_msg_int(msg_id,interval,target=0))
        self._uart.write(cmd)


    def send_set_servo_cmd(self,servo,pwm):
        '''Send command messsage to set values of individual servos'''
        cmd = self._build_msg_cmd_long(183,params=self._build_frame_cmd_do_set_servo(servo,pwm))
        self._uart.write(cmd)


    def __cntl_to_pwm(self,value):
        '''Helper to convert -1 -- 1 values of controls to PWM values (us)'''
        return(400*value+1500)


    def setControls(self,controls):
        '''Aend corresponding mavlink message to set servo values based on current settings of controls object'''
        self.send_set_servo_cmd(YAW_SERVO,self.__cntl_to_pwm(controls.yaw)) #YAW Servo Channel 2
        self.send_set_servo_cmd(THROTTLE_SERVO,self.__cntl_to_pwm(controls.throttle)) #THROTTLE Servo Channel 1
        self.send_set_servo_cmd(UP_SERVO,self.__cntl_to_pwm(controls.up)) #UP Servo Channel 3

    def _read_uart(self):
        '''Read contents of serial buffer and parse messages'''
        result = self._uart.readinto(self.ser_buf)
        if result == None:
            print("Nothing Read.")







