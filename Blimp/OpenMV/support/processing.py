

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


def parseSensorData():  # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    output = 0
    print("parsing sensor data")

    parseIrSensorData()
    dataClasses.data.colorDetected = imageProcessing.colorDetectedByCamera(
        dataClasses.rawData.img)

    print("color detected: " + dataClasses.data.colorDetected)

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

    print('ir sensor: ' + str(dataClasses.data.irData))


def parseLidarData():
    print('>>>>>>>>>>>>>>>')
    print('LIDAR DATA')
    print('>>>>>>>>>>>>>>>')
    print(dataClasses.rawData.lidar_cm )
    if (dataClasses.rawData.lidar_cm != None):
        rawDist_ft = dataClasses.rawData.lidar_cm / 30.48
        correctedDist_ft = attitudeCorrectDistance(
            rawDist_ft, dataClasses.rawData.imu_roll, dataClasses.rawData.imu_pitch)
        dataClasses.data.lidarDistance_ft = correctedDist_ft
        print('lidar distance (ft): ' + str(correctedDist_ft))


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
    currentValue = dataClasses.rawData.rc_sw_door
    if currentValue is not None:
        # Iterate over states, setting state appropriately
        # Split up range evenly
        currentDelta = 500 / (len(dataClasses.DoorControlState()) - 1)
        for state in dataClasses.DoorControlState():
            if state[0] + currentDelta >= currentValue and state[0] - currentDelta <= currentValue:
                dataClasses.data.sw_door_control = state[1]
                break
        else:   # I hate for/else loops but this is a good way of handling an unexpected error
            dataClasses.data.sw_door_control = None

    currentValue = dataClasses.rawData.rc_sw_flt_mode
    if currentValue is not None:
        currentDelta = 500 / (len(dataClasses.FlightModeState()) - 1)
        for state in dataClasses.FlightModeState():
            if state[0] + currentDelta >= currentValue and state[0] - currentDelta <= currentValue:
                dataClasses.data.sw_flight_mode = state[1]
                break
        else:
            dataClasses.data.sw_flight_mode = None

    # There's no switch for this in ProcessedData.
    # currentValue = dataClasses.rawData.rc_sw_st_cntl
    # currentDelta = 500 / (len(dataClasses.AutonomousModeState()) - 1)
    # for state in dataClasses.AutonomousModeState():
    #     if state[0] + currentDelta >= currentValue and state[0] - currentDelta <= currentValue:
    #         pass
    #         break
    # else:
    #     pass


# def distanceToBall():

# def distanceToCeiling():


# def distanceToFloor(): #may not actually ever do this one.


# def distanceToGoal():
