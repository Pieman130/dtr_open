# MAVLink OpticalFlow Script.
#
# This script sends out OpticalFlow detections using the MAVLink protocol to
# an ArduPilot/PixHawk controller for position control using your OpenMV Cam.
#
# P4 = TXD

import image, math, pyb, sensor, struct, time
import logger

# Parameters #################################################################

uart_baudrate = 115200

MAV_system_id = 1
MAV_component_id = 0x54
MAV_OPTICAL_FLOW_confidence_threshold = 0.1  # Below 0.1 or so (YMMV) and the results are just noise.

##############################################################################

# LED control
led = pyb.LED(2) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
led_state = 0

def update_led():
    global led_state
    led_state = led_state + 1
    if led_state == 10:
        led.on()
    elif led_state >= 20:
        led.off()
        led_state = 0

# Link Setup

uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)

# Helper Stuff

packet_sequence = 0

def __checksum(data, extra): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    output = 0xFFFF
    for i in range(len(data)):
        tmp = data[i] ^ (output & 0xFF)
        tmp = (tmp ^ (tmp << 4)) & 0xFF
        output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    tmp = extra ^ (output & 0xFF)
    tmp = (tmp ^ (tmp << 4)) & 0xFF
    output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    return output


def __msg_frame(msg_id, extra_crc, payload, pkt_seq, sys_id=1, comp_id=1):
    payload_len = len(payload)
    msg = struct.pack("<BBBBB{}s".format(payload_len), #combine payload with other packet data, from https://mavlink.io/en/guide/serialization.html#v1_packet_format
                        payload_len,
                        pkt_seq & 0xFF,
                        sys_id,
                        comp_id,
                        msg_id,
                        payload)

    return struct.pack("<B{}sH".format(5+payload_len),
                        0xFE,
                        msg,
                        __checksum(msg,extra_crc))

def parse_mavlink(ser_msg):
    '''
    0th B = preamble (254)
    1st B = payload length
    2nd B = seq #
    3rd B = sys id
    4th B = Comp id
    5th B = Msg id (message type)
    6th - n B = payload
    n-2 = 1st byte chksum
    n-1 = 2nd byte chksum
    '''
    header = []
    try:
        for i in range(6):
            header.append(ser_msg[i])
        if ser_msg[0] != 254: #if inital byte not 254, it is misaligned message, ignore
            return None
        else:
            logger.log.verbose("Payload Length: ", ser_msg[1])
            logger.log.verbose("Message Type: ", ser_msg[5])

        payload = ser_msg[6:-2]
        logger.log.verbose("Payload: ", payload)
        logger.log.verbose("Checksum: ", "Bytes: ", ser_msg[-2:], "Int: ", ser_msg[-2], ser_msg[-1])
        logger.log.verbose("Total Packet Len: ", len(ser_msg))
        logger.log.verbose("---------------------")
    except IndexError:
        return None

MAV_OPTICAL_FLOW_message_id = 100
MAV_OPTICAL_FLOW_id = 0 # unused
MAV_OPTICAL_FLOW_extra_crc = 175

# http://mavlink.org/messages/common#OPTICAL_FLOW
# https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_optical_flow.h

def mvlnk_param_req_lst(packet_sequence):
    '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_param_request_list.h'''
    system_id = 1 #1 is main flight controller
    component_id = 1 #not sure what "1" is, but hopefully it is the main component of the flight controller
    payload = struct.pack("<bb",system_id,component_id) #payload format from https://mavlink.io/en/messages/common.html#PARAM_REQUEST_LIST
    
    return __msg_frame(21,159,payload,packet_sequence)


def mvlnk_manual_control(packet_sequence, x=0, #pitch (fwd/bk of right stick)
                                          y=0, #roll (left/right of right stick)
                                          z=0, #thrust (fwd/bk of left stick)
                                          r=0, #yaw (left/right of left stick)
                                          buttons=0): #8-bit bitfield
    '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_manual_control.h'''
    target = 0 #target system to be controlled #TODO what does this mean?
    payload = struct.pack("<hhhhHB",x,y,z,r,buttons,target) 
    
    return __msg_frame(69,243,payload,packet_sequence)


def mvlink_ch_overide(packet_sequence, ch=(0,0,0,0,0,0,0,0)):
    '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_rc_channels_override.h'''
    target_system = 1
    target_component = 1
    payload = struct.pack("<8HBB",ch[0],ch[1],ch[2],ch[3],ch[4],ch[5],ch[6],ch[7],
                            target_system,target_component)

    return __msg_frame(70,124,payload,packet_sequence)

def mvlink_cmd_long(packet_sequence,cmd,params=[float('NaN')]*7):
    '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_command_long.h'''
    if len(params)<7:
        logger.log.verbose("ERROR: command_long message requires exactly 7 parameters, unused param locations should be filled with NaN.")
        return False
    target_system = 1
    target_component = 1 #TODO maybe "0"?
    confirm = 0 #TODO nonzero for retransmits
    payload = struct.pack("<7fHBBB",params[0],params[1],params[2],params[3],
                                    params[4],params[5],params[6],
                                    cmd,target_system,target_component,confirm)

    return __msg_frame(76,152,payload,packet_sequence)

def mv_set_msg_int(id,inter,target=0):
    '''Set params for mav_cmd_set_message_interval #511
    id = message number
    inter = interval in usec'''
    return [id,inter,float('Nan'),float('NaN'),float('NaN'),float('NaN'),target]

def mv_cmd_req_msg(id):
    '''Set params for mav_cmd_request_message #512'''
    return [id,float('Nan'),float('NaN'),float('NaN'),float('NaN'),float('NaN'),float('NaN')]

def mv_cmd_do_set_servo(servo_ch,value):
    '''Set params for mav_cmd_do_set_servo #183
    servo_ch= servo channel number
    value = PWM value (us)
    '''
    return [servo_ch,value,float('NaN'),float('NaN'),float('NaN'),float('NaN'),float('NaN')]

def send_msg(msg):
    uart.write(msg)
    update_led()

clock = time.clock()   

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.B64X32) # Set frame size to 64x32... (or 64x64)...
sensor.skip_frames(time = 2000)     # Wait for settings take effect.

packet_sequence = 0

#msg = mvlink_ch_overide(packet_sequence, (1000,1000,1000,1000,1000,1000,1000,1000))
msg = mvlink_cmd_long(packet_sequence,511,params=mv_set_msg_int(35,10000)) #35 rc channel values
send_msg(msg)

msg = mvlink_cmd_long(packet_sequence,511,params=mv_set_msg_int(30,10000)) #30 attitude values
send_msg(msg)

msg = mvlink_cmd_long(packet_sequence,511,params=mv_set_msg_int(36,10000)) #30 attitude values
send_msg(msg)

msg = mvlink_cmd_long(packet_sequence,511,params=mv_set_msg_int(132,90000)) #132 distance sensor
send_msg(msg)

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.


    
    msg = mvlnk_manual_control(packet_sequence,x=500,y=0,z=0,r=0,buttons=0)
    send_msg(msg)
    #t_start = time.time()
    time.sleep(0.5)
    msg = mvlnk_manual_control(packet_sequence, x=0, #pitch (fwd/bk of right stick)
                                          y=0, #roll (left/right of right stick)
                                          z=500, #thrust (fwd/bk of left stick)
                                          r=0, #yaw (left/right of left stick)
                                          buttons=0) #8-bit bitfield
    send_msg(msg)
    #t_start = time.time()
    time.sleep(0.5)
    msg = mvlnk_manual_control(packet_sequence, x=0, #pitch (fwd/bk of right stick)
                                          y=0, #roll (left/right of right stick)
                                          z=0, #thrust (fwd/bk of left stick)
                                          r=500, #yaw (left/right of left stick)
                                          buttons=0) #8-bit bitfield
    send_msg(msg)
    time.sleep(0.5)
    msg = mvlnk_manual_control(packet_sequence, x=0, #pitch (fwd/bk of right stick)
                                          y=0, #roll (left/right of right stick)
                                          z=0, #thrust (fwd/bk of left stick)
                                          r=0, #yaw (left/right of left stick)
                                          buttons=0) #8-bit bitfield
    send_msg(msg)
    time.sleep(0.5)
    logger.log.verbose("All messages sent!")

    a = uart.readline()
    if a != None:
        parse_mavlink(a)
        try:
            if msg_type == 36:
                #logger.log.verbose("SERVO 4 VALUE: ", int.from_bytes(payload[10:12], "little"))
                pass
            elif msg_type == 132:
                logger.log.verbose("Range: ", int.from_bytes(payload[8:10], "little"))
        except:
            pass
    packet_sequence += 1


