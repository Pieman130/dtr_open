import dataClasses
import time
import mavlink
import logger
if ( dataClasses.config.isMicroPython):
    from pidModule import Controller
else:
    class Controller:
        def __init__(self):
            pass
        def get_pid(self,val,scaler):
            return 0
        def set_pid_gains(self,val):
            pass


class ExitCriteria:
    def __init__(self):
        self.list = []

    def add(self, variableName, value):
        criterion = ExitCriterion(variableName, value)
        self.list.append(criterion)


class ExitCriterion:
    def __init__(self, variableName, value):
        self.variableName = variableName
        self.value = value


class FlightAction:
    def __init__(self, description, controls, exitCriteria, comms, hw):

        self.description = description
        self.timeClock = 0
        self.startTime = None
        self.exitCriteria = exitCriteria
        self.controls = controls
        self.data = dataClasses.data
        self.rawData = dataClasses.rawData
        self.mavlink = comms.mavlink
        self.hw = hw

        self.pid_yaw = Controller()
        self.pid_up = Controller()
        self.pid_throttle = Controller()
        self.ema_alpha = 0.875 #Ema for smoothing LIDAR distance
        self.lidar_ema = 0.0

    def reset(self):
        self.startTime = None
        self.timeClock = 0

    def updateTime(self):
        if self.startTime == None:
            self.startTime = time.time()
        else:
            self.timeClock = time.time() - self.startTime
    def executeNoop(self):
        pass
    def execute(self):

        self.updateTime()
        logger.log.verbose(self.description + " -  Maneuver")
        logger.log.verbose("\ttime: " + str(self.timeClock))

        self.mavlink.setControls(self.controls)

        if dataClasses.data.sw_door_control == "closed":
            self.hw.closeDoor()
        elif dataClasses.data.sw_door_control == "open":
            self.hw.openDoor()
        else:
            # TODO: Implement proper autonomous door control
            if self.controls.servo == 1:
                self.hw.openDoor()
            else:
                self.hw.closeDoor()

        logger.log.info("Controls Values: {}".format(self.controls.printValues()))

    def sendNoop(self):
        blankControls = Controls()
        self.mavlink.setControls(blankControls)

    def isExitCriteriaMet(self):
        if self.isManeuverTimeoutReached() or self.isSensorExitCriteriaMet():
            return True
        else:
            return False

    def isSensorExitCriteriaMet(self):
        numCriterionUnmet = 0
        numCriterionMet = 0
        for item in self.exitCriteria.list:
            if not self.isCriteriaTimeClock(item.variableName):
                if item.value == self.getProperty(item.variableName):
                    numCriterionMet = numCriterionMet + 1
                else:
                    logger.log.verbose("NO MATCH (" + item.variableName + ") = " + str(item.value) + " != " + str(self.getProperty(item.variableName)))
                    numCriterionUnmet = numCriterionUnmet + 1

        if numCriterionUnmet == 0 and numCriterionMet > 0:
            return True
        else:
            return False

    def isManeuverTimeoutReached(self):
        returnVal = False
        for item in self.exitCriteria.list:
            if self.isCriteriaTimeClock(item.variableName):
                if self.timeClock > item.value:
                    returnVal = True

        return returnVal

    def isCriteriaTimeClock(self, value):
        if value == "timeClock":
            return True
        else:
            return False

    def getProperty(self, name):
        if name == "timeClock":
            return getattr(self, name)
        else:
            return getattr(self.data, name)

    def assistedAltitudeWebControlled(self):
        logger.log.info("TRYING TO HOVER AT ALTITUDE: " + str(dataClasses.gndStationCmd.manualHeight) + " cm")
        self.execute_assisted_altitude(dataClasses.gndStationCmd.manualHeight)

    def execute_assisted_altitude(self, height):
        '''take in desired distance to ceiling (height)
        maintain a pid controlled hover about that distance'''
        logger.log.info("executing assisted altitude to height: " + str(height))
        if self.data.lidarDistance != None:   

            if ( dataClasses.config.isMicroPython):                
                self.pid_up.set_pid_gains(p = dataClasses.gndStationCmd.p_up)
                self.pid_up.error_rounding_up = dataClasses.gndStationCmd.error_rounding_up
                self.pid_up.error_scaling_up = dataClasses.gndStationCmd.error_scaling_up
                self.pid_up.pid_minimum = dataClasses.gndStationCmd.pid_min_up
 
            else:
                p = dataClasses.gndStationCmd.p_up
                self.pid_up.set_pid_gains(p)  

            #logger.log.verbose("right before get pid")
            self.controls.up = self.pid_up.get_pid(self.data.lidarDistance-height,scaler= dataClasses.gndStationCmd.scalar_up)   
                                  
           # self.lidar_ema = self.ema_alpha * self.lidar_ema + (1 - self.ema_alpha) * self.data.lidarDistance

           # logger.log.verbose("ema alpha: " + str(self.ema_alpha) + ", lidarEma: " + str(self.lidar_ema))
            #self.controls.up = self.pid_up.get_pid(self.lidar_ema-height,scaler= dataClasses.gndStationCmd.scalar_up)             

            logger.log.info("Executing Assisted Altitude.  PID Up Value: {}".format(self.controls.up) )
       

    def execute_yaw_control(self, desired_yaw_rate):
        '''take in desired yaw_rate from attitude message
        and maintain a pid controlled yaw'''
        logger.log.info("executing yaw rate control.  Desired yaw rate: " + str(desired_yaw_rate))
        if self.rawData.imu_yaw_rate != None:

            if (dataClasses.config.isMicroPython):                
                self.pid_yaw.set_pid_gains(p = dataClasses.gndStationCmd.p_yaw)
                self.pid_yaw.error_rounding_up = dataClasses.gndStationCmd.error_rounding_yaw
                self.pid_yaw.error_scaling_up = dataClasses.gndStationCmd.error_scaling_yaw
                self.pid_yaw.pid_minimum = dataClasses.gndStationCmd.pid_min_yaw
 
            else:
                p = dataClasses.gndStationCmd.p_yaw
                self.pid_yaw.set_pid_gains(p)  

            self.controls.yaw = self.pid_yaw.get_pid(self.rawData.imu_yaw_rate-desired_yaw_rate,scaler=dataClasses.gndStationCmd.scalar_yaw)
            logger.log.info("Executing Yaw Rate Control.  PID Yaw Value: {}".format(self.controls.yaw) )

class Controls:
    def __init__(self):
        self.yaw = 0  # -1 to 1
        self.up = 0  # -1 to 1
        self.throttle = 0  # -1 to 1
        self.servo = 0  # 0 for OFF. 1 for ON.

    def printValues(self):
        logger.log.verbose("\t\tyaw: " + str(self.yaw))
        logger.log.verbose("\t\tup: " + str(self.up))
        logger.log.verbose("\t\tthrottle: " + str(self.throttle))
        logger.log.verbose("\t\tservo: " + str(self.servo))
