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

rawData = RawData()



class ProcessedData:
    def __init__(self):
        self.irData = None
        self.colorDetected = None
        self.distanceToBall = None
        self.aprilTagDetected = None

data = ProcessedData()