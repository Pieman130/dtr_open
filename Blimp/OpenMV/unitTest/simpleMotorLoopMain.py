import time
import hardware

import pyb
UART_BAUDRATE = 115200
UART_TIMEOUT = 1000


HW_UART = 3
class Controls:
    def __init__(self):
        self.yaw = 0  # -1 to 1
        self.up = 0  # -1 to 1
        self.throttle = 0  # -1 to 1
        self.servo = 0  # 0 for OFF. 1 for ON.

class SimpleHw:
    def __init__(self):
        self.uart = pyb.UART(HW_UART)
        self.uart.init(UART_BAUDRATE, timeout=UART_TIMEOUT, bits=8, parity=None, stop=1, flow=0, read_buf_len=64)

hw = SimpleHw()

#UART_BAUDRATE = 115200
#UART_TIMEOUT = 1000
#HW_UART = 3
#import pyb
#uart = pyb.UART(HW_UART)
#uart.init(UART_BAUDRATE, timeout=UART_TIMEOUT, bits=8, parity=None, stop=1, flow=0) #, read_buf_len=64)

led = hardware.Led()
import mavlink
import logger
logger.log.setLevel_verbose()

mav = mavlink.MavLink(hw)
ctrl = Controls()
r = hw.uart.readline()
print(r)

while(True):


    time.sleep(0.2)
    led.turnOn('blue')
    print("led blue")
    ctrl.up = 0.5
    mav.setControls(ctrl)

   # r = hw.uart.readline()
   # print(r)

    time.sleep(0.2)
    led.turnOn('green')
    print("led green")
    ctrl.up = -0.5
    mav.setControls(ctrl)

   # r = hw.uart.readline()
  #  print(r)
