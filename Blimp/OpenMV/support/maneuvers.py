#from processing import data
class Silly:
    colorDetected = False
    aprilTagDetected = False

testData = Silly
testData.colorDetected = False

data = testData

TIME_INCREMENT_S = 1

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
        global data
        self.description = description
        self.timeClock = 0
        self.exitCriteria = exitCriteria
        self.controls = controls
        self.data = data

    def execute(self):
        print(self.description + " -  Maneuver")
        print("\t time: " + str(self.timeClock))
        self.controls.printValues()
        self.timeClock = self.timeClock + TIME_INCREMENT_S

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
                    numCriterionUnmet = numCriterionUnmet + 1               

        if numCriterionUnmet == 0:
            return True
        else:
            return False        
    
    def isManeuverTimeoutReached(self):
        returnVal = False
        for item in self.exitCriteria.list:
            if self.isCriteriaTimeClock(item.variableName):
                if item.value == self.timeClock:
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
        self.yaw = 0
        self.up = 0
        self.throttle = 0
        self.servo = 0
    def printValues(self):            
        print("\t\tyaw: " + str(self.yaw))
        print("\t\tup: " + str(self.up))
        print("\t\tthrottle: " + str(self.throttle))
        print("\t\tservo: " + str(self.servo))

