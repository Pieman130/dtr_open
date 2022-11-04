import time
import pyb

LED_RED = 1
LED_GREEN = 2

redLed = pyb.LED(LED_RED)
greenLed = pyb.LED(LED_GREEN)

while(True):
    time.sleep(1.5)    
    print("led green")
    redLed.off()
    greenLed.on()

  

    time.sleep(1.5)
    print("led red")
    redLed.on()
    greenLed.off()
