

# Do processing of sensor data
import logger
import dataClasses
import math
if dataClasses.config.isMicroPython:
    import imageProcessing
else:
    import imageProcessingMock
    imageProcessing = imageProcessingMock

SERVO_OPEN = 0
SERVO_CLOSED = 45


def parseSensorData():  # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    output = 0
    logger.log.verbose("parsing sensor data")

    parseIrSensorData()
    dataClasses.data.colorDetected = 'green'
    
    imageProcessing.find_ball(dataClasses.rawData.img)
    #imageProcessing.find_yellow_goal(dataClasses.rawData.img)
    #imageProcessing.find_orange_goal(dataClasses.rawData.img)

    #imageProcessing.colorDetectedByCamera(
     #   dataClasses.rawData.img)

    logger.log.verbose("color detected: " + dataClasses.data.colorDetected)

    dataClasses.data.aprilTagFound = imageProcessing.lookForAprilTag(
        dataClasses.rawData.img)
    dataClasses.data.isAprilTagDetected = dataClasses.data.aprilTagFound.foundIt

    parseLidarData()

    # overwrite for testing purposes the processed info, to test state machine
    # for running on pc.
    if (dataClasses.config.isMicroPython == False):
        dataClasses.data.colorDetected = dataClasses.gndStationCmd.mockSensor_greenDetected
        dataClasses.data.isAprilTagDetected = dataClasses.gndStationCmd.mockSensor_aprilTagDetected

    return output


def parseIrSensorData():
    dataClasses.data.irData = not bool(dataClasses.rawData.irSensor)

    logger.log.verbose('ir sensor: ' + str(dataClasses.data.irData))


def parseLidarData():
    logger.log.verbose('>>>>>>>>>>>>>>>')
    logger.log.verbose('LIDAR DATA')
    logger.log.verbose('>>>>>>>>>>>>>>>')
    logger.log.verbose(dataClasses.rawData.lidar )
    if (dataClasses.rawData.lidar != None):
        rawDist = dataClasses.rawData.lidar 
        correctedDist_ft = attitudeCorrectDistance(
            rawDist, dataClasses.rawData.imu_roll, dataClasses.rawData.imu_pitch)
        #correctedDist_ft = rawDist
        dataClasses.data.lidarDistance = dataClasses.rawData.lidar
        
        if(dataClasses.data.lidarDistance > 1600):
            dataClasses.data.lidarDistance = 1600 #trimming bogus lidar values

        logger.log.verbose('lidar value = ' + str(rawDist) + ', lidar corr = ' + str(correctedDist_ft) + ',imu_roll = ' + str(dataClasses.rawData.imu_roll) + ', imu_pitch =' + str(dataClasses.rawData.imu_pitch))
        
        logger.log.verbose('lidar distance (ft): ' + str(correctedDist_ft))


def attitudeCorrectDistance(measDist=0.0, roll_rad=0.0, pitch_rad=0.0):
    # correctedDist = math.cos(math.sqrt(roll_rad**2 + pitch_rad**2)) * measDist # Not sure which of these methods will be faster on the uC
    correctedDist = math.cos(roll_rad) * math.cos(pitch_rad) * measDist
    return correctedDist


def parseDoorPosition():
    if dataClasses.rawData.door_position == SERVO_CLOSED:
        dataClasses.data.door_state = 'closed'
    elif door_position == SERVO_OPEN:
        dataClasses.data.door_state = 'open'
    else:
        dataClasses.data.door_state = 'schrodinger'


def parseRCSwitchPositions():
    currentValue = dataClasses.rawData.rc_sw_flt_mode
    if currentValue is not None:
        # Iterate over states, setting state appropriately
        # Split up range evenly
        logger.log.verbose("Beginning Switch Processing")
        logger.log.verbose("Processing door control")
        currentDelta = 250  # Splits things evenly

        flightModes = dataClasses.FlightModeState()

        # If the current value is within +- currentDelta of a mode, set the mode variable to that mode.
        if flightModes.Auto[0] + currentDelta >= currentValue and flightModes.Auto[0] - currentDelta <= currentValue:
            dataClasses.data.sw_flight_mode = flightModes.Auto[1]
        elif flightModes.Assisted[0] + currentDelta >= currentValue and flightModes.Assisted[0] - currentDelta <= currentValue:
            dataClasses.data.sw_flight_mode = flightModes.Assisted[1]
        elif flightModes.Manual[0] + currentDelta >= currentValue and flightModes.Manual[0] - currentDelta <= currentValue:
            dataClasses.data.sw_flight_mode = flightModes.Manual[1]
        else:
            dataClasses.data.sw_flight_mode = "None"


    currentValue = dataClasses.rawData.rc_sw_door
    if currentValue is not None:
        logger.log.verbose("Processing flight mode switch")

        doorStates = dataClasses.DoorControlState()
        currentDelta = 250  # Splits things evenly

        if doorStates.Auto[0] + currentDelta >= currentValue and doorStates.Auto[0] - currentDelta <= currentValue:
            dataClasses.data.sw_door_control = doorStates.Auto[1]
        elif doorStates.Open[0] + currentDelta >= currentValue and doorStates.Open[0] - currentDelta <= currentValue:
            dataClasses.data.sw_door_control = doorStates.Open[1]
        elif doorStates.Closed[0] + currentDelta >= currentValue and doorStates.Closed[0] - currentDelta <= currentValue:
            dataClasses.data.sw_door_control = doorStates.Closed[1]
        else:
            dataClasses.data.sw_door_control = "None"


    logger.log.verbose("Processed data states:")
    logger.log.verbose("DR_CTRL:\t " + str(dataClasses.data.sw_door_control))
    logger.log.verbose("FLT_MDE:\t " + str(dataClasses.data.sw_flight_mode))


# def distanceToBall():

# def distanceToCeiling():


# def distanceToFloor(): #may not actually ever do this one.


# def distanceToGoal():
