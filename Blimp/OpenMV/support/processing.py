import imageProcessing

class ProcessedData:
    def __init__(self):
        self.irData = None
        self.colorDetected = None
        self.distanceToBall = None
        self.foundAprilTag = False

data = ProcessedData()
# Do processing of sensor data
from externalSensors import rawData

def parseSensorData(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    global data
    global rawData
    output = 0
    print("parsing sensor data")

    parseIrSensorData()
    data.colorDetected = imageProcessing.colorDetectedByCamera(rawData.img)
    data.foundAprilTag = imageProcessing.lookForAprilTag(rawData.img)
    #data.foundAprilTag = imageProcessing.lookForAprilTagStupid()

    #print("found april tag: " + data.foundAprilTag)

    return output

def parseIrSensorData():
    global rawData
    data.irData = not bool(rawData.irSensor)    
    
    print('ir sensor: ' + str(data.irData))
   

def distanceToBall():
    global rawData

def distanceToCeiling():
    global rawData


def distanceToFloor(): #may not actually ever do this one.
    global rawData 

def distanceToGoal():
    global rawData