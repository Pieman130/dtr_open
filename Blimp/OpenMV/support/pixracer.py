import mavlink_messages
import pyb
pixracer = None

def initialize():
    global pixracer
    uart_baudrate = 115200
    pixracer = pyb.UART(3, uart_baudrate, timeout_char = 1000)    

def write(msg):
    global pixracer
    print("sending to pixracer: " + str(msg))
    pixracer.write(msg)

def pixracerReadUart(): 
    print("IN PIXRACER READ UART")
    global pixracer
    a = pixracer.readline()
    if a != None:
        print("a is not none!")
        mavlink_messages.parse_mavlink(a)

    #print(a)
    print("AT END OF PIXRACER READ UART")