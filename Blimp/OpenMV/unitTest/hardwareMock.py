
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
        print("uart mock send: " + str(msg))

class IrSensorMock:
    def __init__(self):
        print("ir sensor mock")

    def value(self):
        return random.randint(0,1)

class CameraMock:
    def __init__(self):
        print("camera mock")
        self.RGB565 = 0 #nonsense
        self.QQVGA = 0 #nonsense

    def reset(self):
        print("mock reset camera")

    def set_pixformat(self,pixFormat):
        print("mock set pix format: " + str(pixFormat))

    def set_framesize(self,frameSize):
        print("mock set frame size: " + str(frameSize))
    
    def skip_frames(self, frameTimeSkip):
        print("mock set skip frame time: " + str(frameTimeSkip))
    
    def set_auto_gain(self,isSetAutogain):
        print("mock set autogain: " + str(isSetAutogain))
    
    def set_auto_whitebal(self, isSetAutoWhitebalance):
        print("mock set auto while bal" + str(isSetAutoWhitebalance))

    def snapshot(self):
        print("mock snapshot")

class Hardware:
    def __init__(self):       
        self.wlan = NetworkMock()
        
        self.uart = UartMock()      

        self.irSensor = IrSensorMock()

        self.camera = CameraMock()                                                   