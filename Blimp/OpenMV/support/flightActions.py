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
        self.mavlink = comms.mavlink
        self.hw = hw

        self.pid_yaw = Controller()
        self.pid_up = Controller()
        self.pid_throttle = Controller()

    def reset(self):
        self.startTime = None
        self.timeClock = 0

    def updateTime(self):
        if self.startTime == None:
            self.startTime = time.time()
        else:
            self.timeClock = time.time() - self.startTime

    def execute(self):
        self.updateTime()
        logger.log.verbose(self.description + " -  Maneuver")
        logger.log.verbose("\ttime: " + str(self.timeClock))

        if dataClasses.data.sw_flight_mode == "manual":
            # The Mavlink automatically handles remote control inputs - nothing needed here
            # TODO: Implement raw passthrough
            pass

        elif dataClasses.data.sw_flight_mode == "assisted":
            # Altitude hold and yaw stability ?
            # TODO: Implement actual altitude hold and yaw controls
            self.mavlink.setControls(self.controls)

        else:
            # This is the autonomous section - where the code controls the blimp
            # What should go here? I'm just putting in this code as a boilerplate.
            # TODO: Implement actual autonomous controls.
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

    def execute_assisted_altitude(self, height):
        '''take in desired distance to ceiling (height)
        maintain a pid controlled hover about that distance'''
        logger.log.info("executing assisted altitude to height: " + str(height))
        if self.data.lidarDistance != None:   

            self.pid_up.set_pid_gains(p = dataClasses.gndStationCmd.p_up)            
            self.controls.up = self.pid_up.get_pid(self.data.lidarDistance-height,scaler= dataClasses.gndStationCmd.scalar_up) 
            logger.log.debugOnly("controls.up = " + str(self.controls.up))
            logger.log.info("Executing Assisted Altitude.  PID Up Value: {}".format(self.controls.up) )


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
