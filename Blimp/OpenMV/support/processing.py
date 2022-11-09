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
PI = 3.14159

imageProcessing = imageProcessing.ImageProcessing()

def parseSensorData():  # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    output = 0
    logger.log.verbose("parsing sensor data")

    parseIrSensorData()
    dataClasses.data.colorDetected = 'green'
    
    imageProcessing.find_ball(dataClasses.rawData.img)
    imageProcessing.find_yellow_goal(dataClasses.rawData.img)
   # imageProcessing.find_orange_goal(dataClasses.rawData.img)

    logger.log.verbose("yaw rate: " + str(dataClasses.rawData.imu_yaw_rate))
    logger.log.verbose("imu_yaw: " + str(dataClasses.rawData.imu_yaw))
    logger.log.verbose("motor_yaw: " + str(dataClasses.rawData.motor_yaw))
    
    logger.log.verbose("yaw rate limited: " + str(dataClasses.data.imu_yaw_rate_limited))
    logger.log.verbose("imu_yaw limited: " + str(dataClasses.data.imu_yaw_limited))        
    

    logger.log.debugOnly("imu pitch: " + str(dataClasses.rawData.imu_pitch) )
    logger.log.debugOnly("imu imu_roll: " + str(dataClasses.rawData.imu_roll) )

    logger.log.verbose('yellow x error' + str(dataClasses.data.goal_yellow_goal_xerror) )
    logger.log.verbose('yellow y error' + str(dataClasses.data.goal_yellow_goal_yerror) )

    logger.log.verbose('orange x error' + str(dataClasses.data.goal_orange_goal_xerror) )
    logger.log.verbose('orange x error' + str(dataClasses.data.goal_orange_goal_yerror) )

    logger.log.verbose('ball x error: ' + str(dataClasses.data.ball_xerror) )
    logger.log.verbose('ball y error: '  + str(dataClasses.data.ball_yerror) ) 
    
    logger.log.verbose('ballIsFound: ' + str(dataClasses.data.ballIsFound) )
        

    logger.log.verbose("color detected: " + dataClasses.data.colorDetected)

    logger.log.verbose("orange goal is found: " + str(dataClasses.data.orangeGoalIsFound))
    logger.log.verbose("yellow goal is found: " + str(dataClasses.data.yellowGoalIsFound))


    parseLidarData()

    parseYawData() #corrected for extremely large/small erroneous values


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
        # if correctedDist_ft != None:
        #     dataClasses.data.lidarDistance = correctedDist_ft
        # else:
        

        if( (rawDist > 1600) or rawDist == 0):
            pass
        else:
            dataClasses.data.lidarDistance = rawDist
            logger.log.debugOnly('lidar value = ' + str(rawDist) + ', lidar corr = ' + str(correctedDist_ft) + ',imu_roll = ' + str(dataClasses.rawData.imu_roll) + ', imu_pitch =' + str(dataClasses.rawData.imu_pitch))

        
        
       # logger.log.debugOnly('lidar distance (ft): ' + str(correctedDist_ft))


def attitudeCorrectDistance(measDist=0.0, roll_rad=0.0, pitch_rad=0.0):
    # correctedDist = math.cos(math.sqrt(roll_rad**2 + pitch_rad**2)) * measDist # Not sure which of these methods will be faster on the uC
    if roll_rad != None or pitch_rad != None:
        correctedDist = math.cos(roll_rad) * math.cos(pitch_rad) * measDist
        return correctedDist
    else:
        return None


def parseYawData():
    try:
        if dataClasses.rawData.imu_yaw != None:
            if dataClasses.rawData.imu_yaw > PI:
                dataClasses.data.imu_yaw_limited = PI 
            elif dataClasses.rawData.imu_yaw < -(PI):
                dataClasses.data.imu_yaw_limited = -(PI)
            else:
                dataClasses.data.imu_yaw_limited = dataClasses.rawData.imu_yaw 

        if dataClasses.rawData.imu_yaw_rate != None:
            if dataClasses.rawData.imu_yaw_rate > 2*PI or math.isnan(dataClasses.rawData.imu_yaw_rate):
                dataClasses.data.imu_yaw_limited = 0 
            elif dataClasses.rawData.imu_yaw_rate < -(2*PI):
                dataClasses.data.imu_yaw_rate_limited = 0
            else:
                dataClasses.data.imu_yaw_rate_limited = dataClasses.rawData.imu_yaw_rate 
    except:
        pass


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
            dataClasses.config.controlAuthority = flightModes.Auto[1]
        elif flightModes.Assisted[0] + currentDelta >= currentValue and flightModes.Assisted[0] - currentDelta <= currentValue:
            dataClasses.config.controlAuthority = flightModes.Assisted[1]
        elif flightModes.Manual[0] + currentDelta >= currentValue and flightModes.Manual[0] - currentDelta <= currentValue:
            dataClasses.config.controlAuthority = flightModes.Manual[1]
        else:
            dataClasses.config.controlAuthority = "None"


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
    logger.log.verbose("FLT_MDE:\t " + str(dataClasses.config.controlAuthority))


# def distanceToBall():

# def distanceToCeiling():


# def distanceToFloor(): #may not actually ever do this one.


# def distanceToGoal():
