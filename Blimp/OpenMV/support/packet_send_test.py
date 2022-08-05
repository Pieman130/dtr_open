import image, math, pyb, sensor, struct, time

uart_baudrate = 115200

uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)


def send_msg(msg):
    uart.write(msg)


while True:

    #build packet here
    msg = 'PACKET' #serial packet

    send_msg(msg)
