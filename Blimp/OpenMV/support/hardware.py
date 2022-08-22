import pyb
import network
from machine import Pin
import sensor


UART_BAUDRATE = 115200
UART_TIMEOUT = 1000
HW_UART = 3 

class Hardware:
    def __init__(self):        
        self.wlan = network.WINC() # must go first. on initialize, shares a pin needed only on startup by wifi module
                                   # with ir sensor.
        self.uart = pyb.UART(HW_UART, UART_BAUDRATE, UART_TIMEOUT)          
        self.irSensor = Pin('P6',Pin.IN,Pin.PULL_NONE) # must go second.  if this is set before 
                                                    # wifi module is initialized wifi module will not work.
        self.camera = sensor
