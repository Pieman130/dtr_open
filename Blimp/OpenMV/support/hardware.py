import pyb
import network
from machine import Pin
import sensor


UART_BAUDRATE = 115200
UART_TIMEOUT = 1000
HW_UART = 3
IR_DETECT_PIN = 'P6'
SERVO_PWM_ID = 3 #1-3, corresponding to P7-P9. P7-P8 used by wifi


#led = pyb.LED(3) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
LED_GREEN_FOR_ON = 1
LED_BLUE_FOR_GND_STATION_CONNECTED = 3
LED_RED_FOR_GND_STATION_FAIL_CONNECT = 1

class Hardware:
    def __init__(self):        
        self.wlan = network.WINC() # must go first. on initialize, shares a pin needed only on startup by wifi module
                                   # with ir sensor.
        self.uart = pyb.UART(HW_UART)
        self.uart.init(UART_BAUDRATE, timeout=UART_TIMEOUT, bits=8, parity=None, stop=1, flow=0, read_buf_len=64)
        self.camera = sensor
        # The following must be initialized after wlan as they overload pin assignments in WINC class
        self.irSensor = Pin(IR_DETECT_PIN,Pin.IN,Pin.PULL_NONE)
        self.servo = pyb.Servo(SERVO_PWM_ID)
        self.turnOnPoweredOnLight()
        
    def turnOnPoweredOnLight(self):
        print("TURNING ON GREEN LED!")
        self.led = pyb.LED(LED_GREEN_FOR_ON)
        self.led.on() #

    def turnOnConnectedToGndStationLight(self):
        self.led = pyb.LED(LED_BLUE_FOR_GND_STATION_CONNECTED)
        self.led.on()

    def turnOnNotConnectedToGndStationLight(self):
            self.led = pyb.LED(LED_RED_FOR_GND_STATION_FAIL_CONNECT)
            self.led.on()