#import ulogger
#logger = ulogger.getLogger('extSensors')
#logger.setLevel(ulogger.DEBUG) #DEBUG,INFO,WARNING,ERROR,CRITICAL

import time
import dataClasses

class Sensors:
    def __init__(self):
        self.irSensor = None
        self.camera = None        
        self.lidar = None

sensors = Sensors()

class Lidar():
    def __init__(self,com):
        self.mavlink = com.mavlink
        self.mavlink.send_set_msg_interval_cmd(132,50000)
        print("INITIALIZED")
        time.sleep(0.5)
        
    def getDataFake(self):
        return 144

    def getData(self):    
        msg = self.mavlink._uart.readline()
        
        if msg != None:
            dist = self.mavlink.parse_distance(msg)
        
        else:
            dist = None
        
        return dist


def swInitialization(hw,com): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    
    global sensors
    output = 0
     
    swInitializeCamera(hw)    
    swInitializeLidar(com)
    return output 

def swInitializeLidar(com):
    global sensors
    sensors.lidar = Lidar(com)


def swInitializeCamera(hw):
    global sensors        
    print("initializing camera")

    sensors.camera = hw.camera

    sensors.camera.reset()
    sensors.camera.set_pixformat(sensors.camera.RGB565)
    #sensor.set_framesize(sensor.QVGA)
    sensors.camera.set_framesize(sensors.camera.QQVGA) #needed for april tag detections
    sensors.camera.skip_frames(time = 2000)

    # needed for april tag finder
    sensors.camera.set_auto_gain(False)  # must turn this off to prevent image washout...
    sensors.camera.set_auto_whitebal(False)  # must turn this off to prevent image washout...


def collectData():
    global sensors    
    output = 0
    print("collecting data")
    
    dataClasses.rawData.img = sensors.camera.snapshot()     

    dataClasses.rawData.irSensor = sensors.irSensor.value()    

    dataClasses.rawData.lidar_cm = sensors.lidar.getDataFake()

    print(" DISTANCE " + str(dataClasses.rawData.lidar_cm))
   # data_dict = mavlink.getDataFromPixRacer

  #  mavlink.refreshPixRacerCurrentValues


    return output
