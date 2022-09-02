import dataClasses
import time
import mavlink


class ExitCriteria:
    def __init__(self):
        self.list = []
       
    def add(self,variableName,value):
        criterion = ExitCriterion(variableName,value)
        self.list.append(criterion)

class ExitCriterion:
    def __init__(self,variableName,value):
        self.variableName = variableName
        self.value = value


class FlightAction:
    def __init__(self,description,controls,exitCriteria,comms):
        
        self.description = description
        self.timeClock = 0
        self.startTime = None
        self.exitCriteria = exitCriteria
        self.controls = controls
        self.data = dataClasses.data
        self.mavlink = comms.mavlink

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
        print(self.description + " -  Maneuver")
        print("\ttime: " + str(self.timeClock))                
        self.mavlink.setControls(self.controls)

        self.mavlink._read_uart()
        print("AFTER READ UART!!")
    
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
                    print("NO MATCH (" + item.variableName + ") = " + str(item.value) + " != " + str(self.getProperty(item.variableName)) )                    
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


    def isCriteriaTimeClock(self,value):
        if value == "timeClock":
            return True
        else:
            return False

    def getProperty(self,name):
        if name == "timeClock":
            return getattr(self,name)
        else:
            return getattr(self.data,name)

class Controls:
    def __init__(self):                
        self.yaw = 0 #-1 to 1
        self.up = 0 #-1 to 1
        self.throttle = 0 #-1 to 1
        self.servo = 0 # 0 for OFF. 1 for ON.
    def printValues(self):            
        print("\t\tyaw: " + str(self.yaw))
        print("\t\tup: " + str(self.up))
        print("\t\tthrottle: " + str(self.throttle))
        print("\t\tservo: " + str(self.servo))

