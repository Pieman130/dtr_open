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

class ProcessedData:
    def __init__(self):
        self.irData = None
        self.colorDetected = None
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
        self.p_up = None
        self.i_up = None
        self.d_up = None
        
    def print(self):
        print("manuever desc: " + self.maneuverDescription)
        print("base up: " + str(self.baseUpVal))
        print("duration: " + str(self.duration))


data = ProcessedData()
rawData = RawData()
gndStationCmd = GroundStationCommand()
config = Configuration()
