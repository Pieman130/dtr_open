import imageProcessing

# Do processing of sensor data
import dataClasses

def parseSensorData(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h    
    output = 0
    print("parsing sensor data")

    parseIrSensorData()
    dataClasses.data.colorDetected = imageProcessing.colorDetectedByCamera(dataClasses.rawData.img)

    print("color detected: " + dataClasses.data.colorDetected)

    dataClasses.data.aprilTagFound = imageProcessing.lookForAprilTag(dataClasses.rawData.img)        
    dataClasses.data.isAprilTagDetected = dataClasses.data.aprilTagFound.foundIt
    return output

def parseIrSensorData():    
    dataClasses.data.irData = not bool(dataClasses.rawData.irSensor)    
    
    print('ir sensor: ' + str(dataClasses.data.irData))
   

#def distanceToBall():    

#def distanceToCeiling():
    


#def distanceToFloor(): #may not actually ever do this one.
 

#def distanceToGoal():
 