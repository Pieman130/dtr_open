import image, math, pyb, sensor, struct, time
from mavlink_messages import *

uart_baudrate = 115200

uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)


def send_msg(msg):
    uart.write(msg)


while True:

    #build packet here
    msg = 'PACKET' #serial packet

    send_msg(msg)

    time.sleep(1)

    a = uart.readline()
    if a != None:
        parse_mavlink(a)
