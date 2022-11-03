import pyb
import network
from machine import Pin
import sensor
import logger



UART_BAUDRATE = 115200
UART_TIMEOUT = 50
HW_UART = 3
IR_DETECT_PIN = 'P6'
SERVO_PWM_ID = 3 #1-3, corresponding to P7-P9. P7-P8 used by wifi


#led = pyb.LED(3) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
LED_RED = 1
LED_GREEN = 2
LED_BLUE = 3

SERVO_OPEN = 15
SERVO_CLOSED = 65


class Led:
    def __init__(self):
        self.blueLed = pyb.LED(LED_BLUE)
        self.greenLed = pyb.LED(LED_GREEN)
        self.redLed = pyb.LED(LED_RED)
        self.turnOff()

    def turnOn(self,color):

        if(color == 'blue'):
            self.redLed.off()
            self.greenLed.off()
            self.blueLed.on()
                        
        elif(color == 'red'):
            self.redLed.on()
            self.greenLed.off()
            self.blueLed.off()                        

        elif(color == 'green'):
            self.redLed.off()
            self.greenLed.on()
            self.blueLed.off()                        

        elif(color == 'cyan'):
            self.redLed.off()
            self.greenLed.on()
            self.blueLed.on()                        

        elif(color == 'lightGreen'):
            self.redLed.on()
            self.greenLed.on()
            self.blueLed.off()
                                   
        elif(color == 'purple'):
            self.redLed.on()
            self.greenLed.off()
            self.blueLed.on()                                    
     
    def turnOff(self):
        self.blueLed.off()
        self.greenLed.off()
        self.redLed.off()

class Hardware:
    def __init__(self):  
        self.pyb = pyb     
        self.led = Led() 
        self.wlan = network.WINC() # must go first. on initialize, shares a pin needed only on startup by wifi module
                                   # with ir sensor.
        self.uart = pyb.UART(HW_UART)
        self.uart.init(UART_BAUDRATE, timeout=UART_TIMEOUT, bits=8, parity=None, stop=1, flow=0, read_buf_len=64)
        self.camera = sensor
        # The following must be initialized after wlan as they overload pin assignments in WINC class
        self.irSensor = Pin(IR_DETECT_PIN,Pin.IN,Pin.PULL_NONE)
        self.servo = pyb.Servo(SERVO_PWM_ID)
        self.servo_value_closed = SERVO_CLOSED
        self.servo_value_open = SERVO_OPEN
        
        self.imuSensor = None

        self.turnOnPoweredOnLight()

    def turnOnPoweredOnLight(self):
       self.led.turnOn('purple')

    def turnOnConnectedToGndStationLight(self):
        self.led.turnOn('green')

    def turnOnNotConnectedToGndStationLight(self):
         self.led.turnOn('lightGreen')

    def systemFail(self):
         self.led.turnOn('red')

    def pybReset(self):
        self.pyb.hard_reset()


    def openDoor(self):
        logger.log.verbose("********************")
        logger.log.verbose("OPEN DOOR")
        logger.log.verbose("********************")
        self.servo.angle(SERVO_OPEN)
    
    def closeDoor(self):
        logger.log.verbose("********************")
        logger.log.verbose("CLOSE DOOR")
        logger.log.verbose("********************")
        self.servo.angle(SERVO_CLOSED)

 