

# Do processing of sensor data
import dataClasses
import math
if dataClasses.config.isMicroPython:
    import imageProcessing
else:
    import imageProcessingMock
    imageProcessing = imageProcessingMock

SERVO_OPEN = 0
SERVO_CLOSED = 45

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
    if(dataClasses.rawData.lidar_cm != None):
        rawDist_ft = dataClasses.rawData.lidar_cm /30.48
        correctedDist_ft = attitudeCorrectDistance(rawDist_ft, dataClasses.rawData.imu_roll, dataClasses.rawData.imu_pitch)
        dataClasses.data.lidarDistance_ft = correctedDist_ft
        print('lidar distance (ft): ' + str(correctedDist_ft))


def attitudeCorrectDistance(measDist=0.0,roll_rad=0.0,pitch_rad=0.0):
    # correctedDist = math.cos(math.sqrt(roll_rad**2 + pitch_rad**2)) * measDist # Not sure which of these methods will be faster on the uC
    correctedDist = math.cos(roll_rad) * math.cos(pitch_rad) * measDist
    return correctedDist


def parseDoorPosition():
    if dataClasses.rawData.door_position == SERVO_CLOSED:
        dataClasses.ProcessedData.door_state = 'closed'
    elif door_position == SERVO_OPEN:
        dataClasses.ProcessedData.door_state = 'open'
    else:
        dataClasses.ProcessedData.door_state = 'schrodinger'


def parseRCSwitchPositions():
    pass

#def distanceToBall():    

#def distanceToCeiling():
    


#def distanceToFloor(): #may not actually ever do this one.
 

#def distanceToGoal():
 