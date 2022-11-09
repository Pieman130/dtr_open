#import ulogger
#logger = ulogger.getLogger('extSensors')
#logger.setLevel(ulogger.DEBUG) #DEBUG,INFO,WARNING,ERROR,CRITICAL

import time
import dataClasses
import logger
if ( dataClasses.config.isMicroPython):
    import cameraSetup
else:
    import cameraSetupMock
    cameraSetup = cameraSetupMock
    dataClasses.rawData.lidar = 1


class Sensors:
    def __init__(self,hw,com):
        self.hw = hw
        self.mavlink = com.mavlink

        self.irSensor = hw.irSensor
        self.camera = None        
        self.lidar = None
        self.imuSensor = None

        logger.log.verbose("before sw initialize")
        self.swInitializeCamera()
       
        time.sleep(0.5)
        

    def swInitializeCamera(self):       
        self.camera = cameraSetup.OpenMVcamera(self.hw.camera)              

    def collectData(self):

       
        #self.hw.pybReset()
        #print('PYB HARDWARE RESET DONE')
    
        #logger.log.verbose("collecting data")
        
        dataClasses.rawData.img = self.camera.snapshot()     

    
        #dataClasses.rawData.imu_pitch = sensors.imuSensor.getRoll()
        #dataClasses.rawData.imu_yaw = sensors.imuSensor.getPitch()
        #dataClasses.rawData.imu_roll = sensors.imuSensor.getYaw()
        dataClasses.rawData.irSensor = self.irSensor.value()    
        

        start = time.time_ns()
        current_raw_sensor_data = self.mavlink.getSensors()  
        mavlinkTimeNs = time.time_ns() - start
        mavlinkTime = mavlinkTimeNs/1e9
        
       # maxTime = 0.4
       # delayTime = maxTime - mavlinkTime
        logger.log.info('MAVLINK TOTAL TIME: ' + str(mavlinkTime))          
        #time.sleep(delayTime)

            
        

        if current_raw_sensor_data['Attitude'] != None:
            dataClasses.rawData.imu_yaw = current_raw_sensor_data['Attitude']['yaw']
            dataClasses.rawData.imu_pitch = current_raw_sensor_data['Attitude']['pitch']
            dataClasses.rawData.imu_roll = current_raw_sensor_data['Attitude']['roll']
            dataClasses.rawData.imu_yaw_rate = current_raw_sensor_data['Attitude']['yaw_speed']
            dataClasses.rawData.imu_pitch_rate = current_raw_sensor_data['Attitude']['pitch_speed']
            dataClasses.rawData.imu_roll_rate = current_raw_sensor_data['Attitude']['roll_speed']

        if current_raw_sensor_data['RCCH'] != None:
            dataClasses.rawData.rc_sw_door = current_raw_sensor_data['RCCH']['ch7'] 
            dataClasses.rawData.rc_sw_flt_mode = current_raw_sensor_data['RCCH']['ch5'] 
            dataClasses.rawData.rc_sw_st_cntl = current_raw_sensor_data['RCCH']['ch6'] 

            logger.log.verbose("Raw data states:")
            logger.log.verbose("DR_CTRL:\t " + str(dataClasses.rawData.rc_sw_door))
            logger.log.verbose("FLT_MDE:\t " + str(dataClasses.rawData.rc_sw_flt_mode))
            logger.log.verbose("ST_CNTL:\t " + str(dataClasses.rawData.rc_sw_st_cntl))

        if current_raw_sensor_data['Servo'] != None:
            dataClasses.rawData.motor_throttle = current_raw_sensor_data['Servo']['servo1'] 
            dataClasses.rawData.motor_yaw = current_raw_sensor_data['Servo']['servo2'] 
            dataClasses.rawData.motor_up = current_raw_sensor_data['Servo']['servo3'] 

        if current_raw_sensor_data['Lidar'] != None:
            dataClasses.rawData.lidar = current_raw_sensor_data['Lidar']
            
            logger.log.info("lidar distance: " + str(dataClasses.rawData.lidar))


        dataClasses.rawData.door_position = self.hw.servo.angle()
            
            
        logger.log.verbose("motor up value = " + str(dataClasses.rawData.motor_up))       
      