#import ulogger
#logger = ulogger.getLogger('extSensors')
#logger.setLevel(ulogger.DEBUG) #DEBUG,INFO,WARNING,ERROR,CRITICAL

import time
import dataClasses


class Sensors:
    def __init__(self,hw,com):
        self.hw = hw
        self.mavlink = com.mavlink

        self.irSensor = None
        self.camera = None        
        self.lidar = None
        self.imuSensor = None

        self.swInitializeCamera()

        print("INITIALIZED")
        time.sleep(0.5)
        

    def getDataFake(self):
        return 144


    def swInitializeCamera(self): 
        print("initializing camera")

        self.camera = self.hw.camera

        self.camera.reset()
        self.camera.set_pixformat(sensors.camera.RGB565)
        #sensor.set_framesize(sensor.QVGA)
        self.camera.set_framesize(sensors.camera.QQVGA) #needed for april tag detections
        self.camera.skip_frames(2000)

        # needed for april tag finder
        self.camera.set_auto_gain(False)  # must turn this off to prevent image washout...
        self.camera.set_auto_whitebal(False)  # must turn this off to prevent image washout...


    def collectData(self):
    
        print("collecting data")
        
        dataClasses.rawData.img = self.camera.snapshot()     

    
    #dataClasses.rawData.imu_pitch = sensors.imuSensor.getRoll()
    #dataClasses.rawData.imu_yaw = sensors.imuSensor.getPitch()
    #dataClasses.rawData.imu_roll = sensors.imuSensor.getYaw()
        #dataClasses.rawData.irSensor = self.irSensor.value()    

        current_raw_sensor_data = self.mavlink.getSensors()

        dataClasses.rawData.imu_yaw = current_raw_sensor_data['Attitude']['yaw']
        dataClasses.rawData.imu_pitch = current_raw_sensor_data['Attitude']['pitch']
        dataClasses.rawData.imu_roll = current_raw_sensor_data['Attitude']['roll']

        dataClasses.rawData.rc_sw_door = current_raw_sensor_data['RCCH']['ch7'] 
        dataClasses.rawData.rc_sw_flt_mode = current_raw_sensor_data['RCCH']['ch6'] 
        dataClasses.rawData.rc_sw_st_cntl = current_raw_sensor_data['RCCH']['ch5'] 

        dataClasses.rawData.motor_throttle = current_raw_sensor_data['Servo']['servo1'] 
        dataClasses.rawData.motor_yaw = current_raw_sensor_data['Servo']['servo2'] 
        dataClasses.rawData.motor_up = current_raw_sensor_data['Servo']['servo3'] 
        
        dataClasses.rawData.lidar_cm = current_raw_sensor_data['Lidar']

      