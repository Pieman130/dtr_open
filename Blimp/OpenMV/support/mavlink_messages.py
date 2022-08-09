#Mavlink Vers 1 Message functions for
## Checksum
## Paramerter Request List
## Manual control
## ELSE??

#NOTE: All Mavlink serial messages follow this format: https://mavlink.io/en/guide/serialization.html#v1_packet_format
#NOTE: packet_sequence is the monotonically increasing integer value of the message being sent

import struct

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
            print("Payload Length: ", ser_msg[1])
            print("Message Type: ", ser_msg[5])

        payload = []
        for i in range(ser_msg[1]):
            payload.append(ser_msg[6+i])
        print("Payload: ", payload)
        print("Checksum: ", ser_msg[-2], ser_msg[-1])
        print("Total Packet Len: ", len(ser_msg))
        print("---------------------")
    except IndexError:
        return None


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
        print("ERROR: command_long message requires exactly 7 parameters, unused param locations should be filled with NaN.")
        return False
    target_system = 1
    target_component = 1 #TODO maybe "0"?
    confirm = 0 #TODO nonzero for retransmits
    payload = struct.pack("<8fHBBB",params[0],params[1],params[2],params[3],
                                    params[4],params[5],params[6],
                                    cmd,target_system,target_component,confirm)

    return __msg_frame(76,152,payload,packet_sequence)

def mv_set_msg_int(id,inter,target=0):
    '''Set params for mav_cmd_set_message_interval #511'''
    return [id,inter,float('Nan'),float('NaN'),float('NaN'),float('NaN'),target]

def mv_cmd_req_msg(id):
    '''Set params for mav_cmd_request_message #512'''
    return [id,float('Nan'),float('NaN'),float('NaN'),float('NaN'),float('NaN'),float('NaN')]





#def mvlnk_