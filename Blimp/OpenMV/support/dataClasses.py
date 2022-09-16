class Configuration:
    def __init__(self):
        self.isMicroPython = None

class RawData:
    def __init__(self):
        self.img = None
        self.irSensor = None
        self.imu_yaw = None
        self.imu_pitch = None
        self.imu_roll = None
        self.motor_throttle = None 
        self.motor_up = None 
        self.motor_yaw = None 
        self.lidar_cm = None

class ProcessedData:
    def __init__(self):
        self.irData = None
        self.goalColorChoice = None
        self.goalColorDetected = None
        self.isBallDetected = None
        self.ballx = None
        self.bally = None
        self.goalx = None
        self.goaly = None
        self.goalskew = None
        self.distanceToBall = None
        self.aprilTagFound = None
        self.isAprilTagDetected = None
        self.lidarDistance_ft = None        

class GroundStationCommand:
    def __init__(self):
        self.firstManeuver = None
        self.secondManeuver = None
        self.baseUpVal = None
        self.duration = None
        self.mockSensor_greenDetected = ''
        self.mockSensor_aprilTagDetected = ''        
    def print(self):
        print("manuever desc: " + self.maneuverDescription)
        print("base up: " + str(self.baseUpVal))
        print("duration: " + str(self.duration))

data = ProcessedData()
rawData = RawData()
gndStationCmd = GroundStationCommand()
config = Configuration()
