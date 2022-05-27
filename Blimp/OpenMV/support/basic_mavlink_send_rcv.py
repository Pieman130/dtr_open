# MAVLink Send/Rcv example

import image, math, pyb, sensor, struct, time

# Parameters #################################################################

uart_baudrate = 115200


# Link Setup

uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)

# Helper Stuff

packet_sequence = 0

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
            bytes_payload = bytearray(b'')
            for i in range(ser_msg[1]):
                payload.append(ser_msg[6+i])
                bytes_payload.append(ser_msg[6+i])
            print("System ID: ", ser_msg[3])
            print("Component ID: ", ser_msg[4])
            print("Payload: ", payload)
            print("Bytes Payload: ", bytes_payload)
            print("Checksum: ", int.from_bytes(ser_msg[-2:], 'little'))
            print("Total Packet Len: ", len(ser_msg))
            print("------------------------------------------------")
    except IndexError:
        return None


packet_sequence = 0
def send_param_req_lst():

    message_id = 21
    msg_id = 0
    extra_crc = 159 #from https://github.com/mavlink/c_library_v1/blob/master/common/mavlink_msg_param_request_list.h
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
    msg_w_crc = struct.pack("<b7sh",
                           0xFE, #packet start marker
                           msg,  #msg headers with payload
                           checksum(msg,extra_crc)) #calculated checksum taken from mavlink_opticalflow_1.py example

    uart.write(msg_w_crc) #send serial message over uart

#random image capture stuff not used for this packet sender/receiver demo
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.B64X32) # Set frame size to 64x32... (or 64x64)...
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.



time_start = time.time()

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.
    if time.time() - time_start > 10.0: #send message every 10 seconds
        send_param_req_lst()
        time_start = time.time()
        packet_sequence += 1 #update packet sequence number

    a = uart.readline() #read current message received in UART buffer
    if a != None:
        parse_mavlink(a) #parse mavlink message into component parts


