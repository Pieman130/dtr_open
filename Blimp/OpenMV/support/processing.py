

# Do processing of sensor data
import dataClasses
if dataClasses.config.isMicroPython:
    import imageProcessing
else:
    import imageProcessingMock
    imageProcessing = imageProcessingMock

def parseSensorData(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h    
    output = 0
    print("parsing sensor data")

    parseIrSensorData()
    dataClasses.data.colorDetected = imageProcessing.colorDetectedByCamera(dataClasses.rawData.img)

    print("color detected: " + dataClasses.data.colorDetected)

    dataClasses.data.aprilTagFound = imageProcessing.lookForAprilTag(dataClasses.rawData.img)        
    dataClasses.data.isAprilTagDetected = dataClasses.data.aprilTagFound.foundIt

    parseLidarData()


    #overwrite for testing purposes the processed info, to test state machine 
    # for running on pc.
    if(dataClasses.config.isMicroPython == False): 
        dataClasses.data.colorDetected = dataClasses.gndStationCmd.mockSensor_greenDetected
        dataClasses.data.isAprilTagDetected = dataClasses.gndStationCmd.mockSensor_aprilTagDetected


    return output

def parseIrSensorData():    
    dataClasses.data.irData = not bool(dataClasses.rawData.irSensor)    
    
    print('ir sensor: ' + str(dataClasses.data.irData))
   

def parseLidarData():
    dataClasses.data.lidarDistance_ft = dataClasses.rawData.lidar_cm /30.48
    print('lidar distance (ft): ' + str(dataClasses.data.lidarDistance_ft))

#def distanceToBall():    

#def distanceToCeiling():
    


#def distanceToFloor(): #may not actually ever do this one.
 

#def distanceToGoal():
 