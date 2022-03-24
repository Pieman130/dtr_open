import time
import board  # comment this out if using pyserial
import busio  # comment this out if using pyserial
import adafruit_tfmini
import serial

# Use hardware uart
uart = serial.Serial("/dev/ttyS0",115200,timeout=1)

# Or, you can use pyserial on any computer
#import serial
#uart = serial.Serial("/dev/ttyS2", timeout=1)

# Simplest use, connect with the uart bus object
tfmini = adafruit_tfmini.TFmini(uart)


while True:
    print("Distance: {} cm at strength {}".format(tfmini.distance, tfmini.strength))
    time.sleep(0.5)
