TIME_INCREMENT_S = 1

## BASE CLASSES ####################
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


class Manuever:
    def __init__(self,exitCriteria):
        self.timeClock = 0
        self.isActive = False
        self.steps = []             
        self.exitCriteria = exitCriteria 
           
    def isExitCriteriaMet(self):
        numCriterionUnmet = 0
        numCriterionMet = 0
        for item in self.exitCriteria.list:
            if item.value == getattr(self,item.variableName):
                numCriterionMet = numCriterionMet + 1           
            else:
                numCriterionUnmet = numCriterionUnmet + 1               

        if numCriterionUnmet == 0:
            return True
        else:
            return False        
  
    def getNextStep(self):
        print ('not defined')

class Action:
    def __init__(self):
        self.description = ""
        self.duration = 0
        self.yaw = 0
        self.up = 0
        self.throttle = 0
        self.servo = 0
    def printAction(self):
        print("\tAction step: " + self.description)        
        print("\t\tyaw: " + str(self.yaw))
        print("\t\tup: " + str(self.up))
        print("\t\tthrottle: " + str(self.throttle))
        print("\t\tservo: " + str(self.servo))
########################

class GoForward(Manuever):
    def __init__(self,duration,speed,exitCriteria):
        Manuever.__init__(self,exitCriteria)        
        forward = Action()
        self.duration = duration #hack
        forward.description = "go forward"        
        # forward.up => could get baseline value to keep from falling, or do outside of this
        forward.throttle = speed
        self.steps.append(forward)

    def getNextAction(self):
        print("don't do anything now")

    def executeNextStep(self):
        print("Go Forward Maneuver")
        print("\t time: " + str(self.timeClock))
        self.steps[0].printAction()
        self.timeClock = self.timeClock + TIME_INCREMENT_S


    ## need to put this  somewhere...
    
    minValue = 1100 #backwards
    midValue = 1500 #0
    fullValue = 1900 #full forward

    # mavlink_messages 
    # #2 = lift
    # #3 = throttle
    # #4 = up

    
    ch = (0,fullValue,fullValue,fullValue,0,0,0,0)

    ctr = ctr + 1
    msgToSend = mavlink_messages.mvlink_ch_overide(ctr,ch)
    
