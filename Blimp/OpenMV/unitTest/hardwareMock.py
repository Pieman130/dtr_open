
import random
import logger

class NetworkMock:
    def __init__(self):
        logger.log.info("network mock")

    def connect(self,ssid,key):
        pass
        #logger.log.info("mock connecting to: " + ssid + ", " + key)

    def ifconfig(self):
        logger.log.info("mock if config")

class ServoMock:
    def __init__(self):
        logger.log.info("servo mock")
    def angle(self):
        return 0

class IMUMock:
    def __init__(self):
        logger.log.info("imu mock")

    def getRoll(self):
        return 0

    def getYaw(self):
        return 0

    def getPitch(self):
        return 0

class UartMock:
    def __init__(self):
        logger.log.info("uart mock")
    
    def write(self,msg):
        pass
       # logger.log.verbose("uart mock send: " + str(msg))

    def read(self,val):
        logger.log.verbose("uart read")

class IrSensorMock:
    def __init__(self):
        logger.log.info("ir sensor mock")

    def value(self):
        return random.randint(0,1)

class CameraMock:
    def __init__(self):
        logger.log.info("camera mock")
        self.RGB565 = 0 #nonsense
        self.QQVGA = 0 #nonsense

    def reset(self):
        logger.log.info("mock reset camera")

    def set_pixformat(self,pixFormat):
        logger.log.info("mock set pix format: " + str(pixFormat))

    def set_framesize(self,frameSize):
        logger.log.info("mock set frame size: " + str(frameSize))
    
    def skip_frames(self, frameTimeSkip):
        logger.log.info("mock set skip frame time: " + str(frameTimeSkip))
    
    def set_auto_gain(self,isSetAutogain):
        logger.log.info("mock set autogain: " + str(isSetAutogain))
    
    def set_auto_whitebal(self, isSetAutoWhitebalance):
        logger.log.info("mock set auto while bal" + str(isSetAutoWhitebalance))

    def snapshot(self):
        logger.log.info("mock snapshot")

class ServoMock:
    def __init__(self):
        pass
    def angle(self):
        pass
class Hardware:
    def __init__(self):       
        self.wlan = NetworkMock()
        
        self.uart = UartMock()      

        self.irSensor = IrSensorMock()
        
        self.imuSensor = IMUMock()

        self.camera = CameraMock()

        self.servo = ServoMock()     


        self.servo = ServoMock()  
        
    def turnOnPoweredOnLight(self):
       logger.log.info("LED GREEN")

    def turnOnConnectedToGndStationLight(self):
        logger.log.info("LED BLUE")        

    def turnOnNotConnectedToGndStationLight(self):
        logger.log.info("LED LIGHT GREEN")

    def openDoor(self):
        logger.log.info("mock open door")
    
    def closeDoor(self):
        logger.log.info("close door")
                               
    def systemFail(self):
        logger.log.info("SYSTEM FAIL TURN ON RED LED!")              