class RawData:
    def __init__(self):
        self.img = None
        self.irSensor = None
        self.imu_yaw = None
        self.imu_pitch = None
        self.imu_roll = None
        self.motor_throttle = None #or do we put this somewhere else?
        self.motor_up = None #or do we put this somewhere else?
        self.motor_yaw = None #or do we put this somewhere else?
        self.lidar = None

class ProcessedData:
    def __init__(self):
        self.irData = None
        self.colorDetected = None
        self.distanceToBall = None
        self.aprilTagFound = None
        self.isAprilTagDetected = None

class GroundStationCommand:
    def __init__(self):
        self.maneuverDescription = None
        self.baseUpVal = None
        self.duration = None
    def print(self):
        print("manuever desc: " + self.maneuverDescription)
        print("base up: " + str(self.baseUpVal))
        print("duration: " + str(self.duration))


data = ProcessedData()
rawData = RawData()
gndStationCmd = GroundStationCommand()

