import sensor

from machine import Pin


# globals
class Sensors:
    def __init__(self):
        self.irSensor = None
        self.camera = None

class RawData:
    def __init__(self):
        self.img = None
        self.irSensor = None

rawData = RawData()
sensors = Sensors()

def initialize(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    global sensors
    output = 0
    print("initialize sensors")
    initializeCamera()
    sensors.irSensor = Pin('P4',Pin.IN,Pin.PULL_NONE)
    return output
    

def initializeCamera():
    global sensors
    print("initializing camera")

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)

    # needed for april tag finder
    sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
    sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...


    sensors.camera = sensor
        


def collectData():
    global sensors
    global rawData
    output = 0
    print("collecting data")
    rawData.img = sensors.camera.snapshot()     

    rawData.irSensor = sensors.irSensor.value()

    return output
