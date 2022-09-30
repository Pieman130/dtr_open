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
        self.lidar_cm = 0
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
        self.lidarDistance_ft = 0                
        self.door_state = None
        self.sw_door_control = 'open'
        self.sw_flight_mode = 'manual'


class GroundStationCommand:
    def __init__(self):
        self.requestedState = None
        self.firstManeuver = None
        self.secondManeuver = None
        self.baseUpVal = None
        self.duration = None
        self.mockSensor_greenDetected = ''
        self.mockSensor_aprilTagDetected = ''
        self.p_up = None
        self.i_up = None
        self.d_up = None
        self.p_throttle = None
        self.i_throttle = None
        self.d_throttle = None
        self.p_yaw = None
        self.i_yaw = None
        self.d_yaw = None
        self.requestedState = None
        self.manual_up = None
        self.manual_throttle = None
        self.manual_yaw = None
        self.manual_servo = None
        self.scalar_up = None
        self.scalar_yaw = None
        self.scalar_throttle = None


    def print(self):
        print("manuever desc: " + self.maneuverDescription)
        print("base up: " + str(self.baseUpVal))
        print("duration: " + str(self.duration))

# These values are based off of RC servo pulse widths. Makes comparing easier.


class AutonomousModeState:
    startInBalloonSeek = [1000, 'balloonSeek']
    startInGoalSeek = [2000, 'goalSeek']

    def __init__(self):
        self.items = [self.startInBalloonSeek, self.startInGoalSeek]
    def __iter__(self):
        return iter(self.items)
    def __next__(self):
        return next(self.items)
    def __len__(self):
        return len(self.items)


class FlightModeState:
    Manual = [2000, 'manual']
    Assisted = [1500, 'assisted']
    Auto = [1000, 'auto']

    def __init__(self):
        self.items = [self.Auto, self.Assisted, self.Manual]
    def __iter__(self):
        return iter(self.items)
    def __next__(self):
        return next(self.items)
    def __len__(self):
        return len(self.items)


class DoorControlState:
    Closed = [2000, 'closed']
    Open = [1500, 'open']
    Auto = [1000, 'auto']

    def __init__(self):
        self.items = [self.Auto, self.Open, self.Closed]
    def __iter__(self):
        return iter(self.items)
    def __next__(self):
        return next(self.items)
    def __len__(self):
        return len(self.items)


data = ProcessedData()
rawData = RawData()
gndStationCmd = GroundStationCommand()
config = Configuration()
