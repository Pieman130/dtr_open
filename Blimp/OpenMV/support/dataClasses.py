class Configuration:
    def __init__(self):
        self.isMicroPython = None


class RawData:
    def __init__(self):
        self.img = None
        self.irSensor = None
        self.imu_yaw = 0
        self.imu_pitch = 0
        self.imu_roll = 0
        self.motor_throttle = None
        self.motor_up = None
        self.motor_yaw = None
        self.lidar_cm = None
        self.rc_sw_door = None
        self.rc_sw_flt_mode = None
        self.rc_sw_st_cntl = None
        self.door_position = None


class ProcessedData:
    def __init__(self):
        self.irData = None
        self.colorDetected = ''
        self.distanceToBall = None
        self.aprilTagFound = None
        self.isAprilTagDetected = None
        self.lidarDistance_ft = None
        self.door_state = None
        self.sw_door_control = 'open'
        self.sw_flight_mode = 'manual'


class GroundStationCommand:
    def __init__(self):
        self.firstManeuver = None
        self.secondManeuver = None
        self.baseUpVal = None
        self.duration = None
        self.mockSensor_greenDetected = ''
        self.mockSensor_aprilTagDetected = ''
        self.p_up = None
        self.i_up = None
        self.d_up = None
        self.requestedMode = None

    def print(self):
        print("manuever desc: " + self.maneuverDescription)
        print("base up: " + str(self.baseUpVal))
        print("duration: " + str(self.duration))

# These values are based off of RC servo pulse widths. Makes comparing easier.


class AutonomousModeState():
    def __init__(self):
        self.startInBalloonSeek = 1000
        self.startInGoalSeek = 2000


class FlightModeState():
    def __init__(self):
        self.Manual = 2000
        self.Assisted = 1500
        self.Auto = 1000


class DoorControlState():
    def __init__(self):
        self.Closed = 2000
        self.Open = 1500
        self.Auto = 1000


data = ProcessedData()
rawData = RawData()
gndStationCmd = GroundStationCommand()
config = Configuration()
