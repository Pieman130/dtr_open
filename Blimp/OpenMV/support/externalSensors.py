import sensor
from machine import Pin

import dataClasses
class Sensors:
    def __init__(self):
        self.irSensor = None
        self.camera = None        

sensors = Sensors()

def initialize(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    global sensors
    output = 0
    print("initialize sensors")
    initializeCamera()
    initializeIrSensor()
    return output 

def initializeIrSensor():
    global sensors
    sensors.irSensor = Pin('P6',Pin.IN,Pin.PULL_NONE)

def initializeCamera():
    global sensors
    print("initializing camera")

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    #sensor.set_framesize(sensor.QVGA)
    sensor.set_framesize(sensor.QQVGA) #needed for april tag detections
    sensor.skip_frames(time = 2000)

    # needed for april tag finder
    sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
    sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...


    sensors.camera = sensor
        


def collectData():
    global sensors    
    output = 0
    print("collecting data")
    
    dataClasses.rawData.img = sensors.camera.snapshot()     

    dataClasses.rawData.irSensor = sensors.irSensor.value()    
   # data_dict = mavlink.getDataFromPixRacer

  #  mavlink.refreshPixRacerCurrentValues


    return output
