import dataClasses
import time



class Mavlink: # TO BE MOVED TO ANOTHER FILE
    def __init__(self):
        self.stuff = None
    
    def setControls(self,controls):
        self.printSetActions(controls)

    def printSetActions(self,controls):
        print("\tsetting yaw: " + str(controls.yaw))
        print("\tsetting up: " + str(controls.up))
        print("\tsetting throttle: " + str(controls.throttle))
        print("\tsetting servo: " + str(controls.servo))
###################################################

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


class Maneuver:
    def __init__(self,description,controls,exitCriteria):
        
        self.description = description
        self.timeClock = 0
        self.startTime = None
        self.exitCriteria = exitCriteria
        self.controls = controls
        self.data = dataClasses.data
        self.mavlink = Mavlink()

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
                    print("NO MATCH: " + str(item.value))
                    print("vs: " + str(self.getProperty(item.variableName)))
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


## maneuvers
forwardExitCriteria = ExitCriteria()
forwardExitCriteria.add("timeClock",10)
forwardExitCriteria.add("colorDetected",'green')

forwardControls = Controls()
forwardControls.throttle = 0.5

forwardOrGreen = Maneuver("Go forward until see green water bottle.",forwardControls,forwardExitCriteria)

##
three60orAprilTagExit = ExitCriteria()
three60orAprilTagExit.add("timeClock",5) #need to figure out how long it takes to do 360...
three60orAprilTagExit.add("isAprilTagDetected",True)
three60orAprilTagCtrls = Controls()
three60orAprilTagCtrls.yaw = 0.5

three60orAprilTag = Maneuver("360 or until see april tag.",three60orAprilTagCtrls,three60orAprilTagExit)

#
hoverExit = ExitCriteria()
hoverExit.add("timeClock",5) #need to figure out how long it takes to do 360...
hoverCtrls = Controls()
hoverCtrls.up = 0.5

hover = Maneuver("hover",hoverCtrls,hoverExit)