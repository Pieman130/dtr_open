import imageProcessing

class ProcessedData:
    def __init__():
        self.irData: None
        self.colorDetected: None

data = ProcessedData
# Do processing of sensor data
from externalSensors import rawData

def parseSensorData(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    global data
    global rawData
    output = 0
    print("parsing sensor data")

    parseIrSensorData()
    data.colorDetected = imageProcessing.colorDetectedByCamera(rawData.img)

    return output

def parseIrSensorData():
    global rawData
    data.irData = not bool(rawData.irSensor)    
    
    print('ir sensor: ' + str(data.irData))
   