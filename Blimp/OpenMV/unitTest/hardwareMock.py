
import random

class NetworkMock:
    def __init__(self):
        print("network mock")

    def connect(self,ssid,key):
        print("mock connecting to: " + ssid + ", " + key)

    def ifconfig(self):
        print("mock if config")

class UartMock:
    def __init__(self):
        print("uart mock")
    
    def write(self,msg):
        print("uart mock send: " + msg)

class IrSensorMock:
    def __init__(self):
        print("ir sensor mock")

    def value(self):
        return random.randint(0,1)

class CameraMock:
    def __init__(self):
        print("camera mock")

    def reset(self):
        print("mock reset camera")

    def set_pixformat(self,pixFormat):
        print("mock set pix format: " + str(pixFormat))

    def set_framesize(self,frameSize):
        print("mock set frame size: " + str(frameSize))
    
    def skip_frames(self, frameTimeSkip):
        print("mock set skip frame time: " + frameTimeSkip)        
    
    def set_auto_gain(self,isSetAutogain):
        print("mock set autogain: " + isSetAutogain)
    
    def set_auto_whitebal(self, isSetAutoWhitebalance):
        print("mock set auto while bal" + isSetAutoWhitebalance)

class Hardware:
    def __init__(self):
        self.uart = None
        self.wlan = None
        self.irSensor = None
        self.camera = None

    def initialize(self):
        self.wlan = NetworkMock()
        
        self.uart = UartMock()      

        self.irSensor = IrSensorMock()

        self.camera = CameraMock()                                                   