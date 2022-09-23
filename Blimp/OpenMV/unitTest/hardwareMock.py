
import random

class NetworkMock:
    def __init__(self):
        print("network mock")

    def connect(self,ssid,key):
        print("mock connecting to: " + ssid + ", " + key)

    def ifconfig(self):
        print("mock if config")

class ServoMock:
    def __init__(self):
        print("servo mock");
    def angle(self):
        return 0

class IMUMock:
    def __init__(self):
        print("imu mock")

    def getRoll(self):
        return 0

    def getYaw(self):
        return 0

    def getPitch(self):
        return 0

class UartMock:
    def __init__(self):
        print("uart mock")
    
    def write(self,msg):
        print("uart mock send: " + str(msg))

    def read(self):
        print("uart read")

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
        
        self.imuSensor = IMUMock()

        self.camera = CameraMock()

        self.servo = ServoMock()     


        
    def turnOnPoweredOnLight(self):
       print("LED GREEN")

    def turnOnConnectedToGndStationLight(self):
        print("LED BLUE")        

    def turnOnNotConnectedToGndStationLight(self):
        print("LED LIGHT GREEN")
                                              