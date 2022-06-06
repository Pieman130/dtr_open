#Mavlink Vers 1 Message functions for
## Checksum
## Paramerter Request List
## Manual control
## ELSE??

#NOTE: All Mavlink serial messages follow this format: https://mavlink.io/en/guide/serialization.html#v1_packet_format

import struct

def checksum(data, extra): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    output = 0xFFFF
    for i in range(len(data)):
        tmp = data[i] ^ (output & 0xFF)
        tmp = (tmp ^ (tmp << 4)) & 0xFF
        output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    tmp = extra ^ (output & 0xFF)
    tmp = (tmp ^ (tmp << 4)) & 0xFF
    output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    return output

def mvlnk_param_req_lst(packet_sequence):
    '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_param_request_list.h'''
    message_id = 21
    extra_crc = 159 
    system_id = 1 #1 is main flight controller
    component_id = 1 #not sure what "1" is, but hopefully it is the main component of the flight controller
    payload = struct.pack("<bb",system_id,component_id) #payload format from https://mavlink.io/en/messages/common.html#PARAM_REQUEST_LIST
    msg = struct.pack("<bbbbb2s", #combine payload with other packet data, from https://mavlink.io/en/guide/serialization.html#v1_packet_format
                      2,
                      packet_sequence & 0xFF,
                      system_id,
                      component_id,
                      message_id,
                      payload)
    return struct.pack("<b7sh",
                           0xFE, #packet start marker
                           msg,  #msg headers with payload
                           checksum(msg,extra_crc)) #calculated checksum taken from mavlink_opticalflow_1.py example

def mvlnk_manual_control(packet_sequence, x=0, #pitch (fwd/bk of right stick)
                                          y=0, #roll (left/right of right stick)
                                          z=0, #thrust (fwd/bk of left stick)
                                          r=0, #yaw (left/right of left stick)
                                          buttons=0) #8-bit bitfield
    '''https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_manual_control.h'''
    message_id = 69
    extra_crc = 243
    payload_len = 11
    system_id = 1 #1 is main flight controller
    target = 0 #target system to be controlled #TODO what does this mean?
    component_id = 1 #not sure what "1" is, but hopefully it is the main component of the flight controller
    payload = struct.pack("<hhhhHB",x,y,z,r,buttons,target) #strict format for payload of mavlink messages
    msg = struct.pack("<bbbbb{}s".format(payload_len), #combine payload with other packet data, from https://mavlink.io/en/guide/serialization.html#v1_packet_format
                      payload_len,
                      packet_sequence & 0xFF,
                      system_id,
                      component_id,
                      message_id,
                      payload)
    return struct.pack("<b{}sh".format(payload_len+5),
                           0xFE, #packet start marker
                           msg,  #msg headers with payload
                           checksum(msg,extra_crc)) #calculated checksum taken from mavlink_opticalflow_1.py example