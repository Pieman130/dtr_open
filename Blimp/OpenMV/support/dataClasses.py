class Configuration:
    def __init__(self):
        self.isMicroPython = None
        self.controlAuthority = 'autonomous'

class RawData:
    def __init__(self):
        self.img = None
        self.irSensor = False
        self.imu_yaw = 0
        self.imu_pitch = 0
        self.imu_roll = 0
        self.imu_yaw_rate = 0
        self.imu_pitch_rate = 0
        self.imu_roll_rate = 0
        self.motor_throttle = None
        self.motor_up = None
        self.motor_yaw = None
        self.lidar = None
        self.rc_sw_door = None
        self.rc_sw_flt_mode = None
        self.rc_sw_st_cntl = None
        self.door_position = None


class ProcessedData:
    def __init__(self):
        self.irData = 0 
        self.colorDetected = ''
        self.goalColorChoice = None
        self.goalColorDetected = None
        self.isBallDetected = None
              
        self.goalskew = None
        self.distanceToBall = None
        self.aprilTagFound = None
        self.isAprilTagDetected = None
        self.lidarDistance = None
        self.door_state = None
        self.sw_door_control = 'open'
        self.sw_flight_mode = 'assisted'

        self.goal_yellow_xerror = None
        self.goal_yellow_goal_yerror = None
        self.goal_orange_xerror = None
        self.goal_orange_goal_yerror = None
        
        self.ball_xerror = None
        self.ball_yerror = None  
        self.ballIsFound = None
        

class GroundStationCommand:
    def __init__(self):
        self.firstManeuver = None
        self.secondManeuver = None
        self.baseUpVal = None
        self.duration = None
        self.mockSensor_greenDetected = ''
        self.mockSensor_aprilTagDetected = ''
        self.p_up = 1
        self.i_up = 0
        self.d_up = 0
        self.p_throttle = 1
        self.i_throttle = 0
        self.d_throttle = 0
        self.p_yaw = 1
        self.i_yaw = 0
        self.d_yaw = 0
        self.manual_up = None
        self.manual_throttle = None
        self.manual_yaw = None
        self.manual_servo = None
        self.scalar_up = 1
        self.scalar_yaw = 1
        self.scalar_throttle = 1
        self.error_rounding_up = 0
        self.error_scaling_up = 1
        self.error_rounding_yaw = 0
        self.error_scaling_yaw = 1
        self.pid_min_up = -0.2
        self.pid_min_yaw = -1.0
        self.controlAuthority = 'autonomous'
        self.manualHeight = 100000
        self.resetOpenMVforFTPtsfr = 0


        self.requestedState = None

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
