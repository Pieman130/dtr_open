import pyb
import network
from machine import Pin
import sensor


UART_BAUDRATE = 115200
UART_TIMEOUT = 1000
HW_UART = 3
IR_DETECT_PIN = 'P6'
SERVO_PWM_ID = 3 #1-3, corresponding to P7-P9. P7-P8 used by wifi


class Hardware:
    def __init__(self):        
        self.wlan = network.WINC() # must go first. on initialize, shares a pin needed only on startup by wifi module
                                   # with ir sensor.
        self.uart = pyb.UART(HW_UART, UART_BAUDRATE, UART_TIMEOUT)
        self.camera = sensor
        # The following must be initialized after wlan as they overload pin assignments in WINC class
        self.irSensor = Pin(IR_DETECT_PIN,Pin.IN,Pin.PULL_NONE)
        self.servo = pyb.SERVO(SERVO_PWM_ID)
        
