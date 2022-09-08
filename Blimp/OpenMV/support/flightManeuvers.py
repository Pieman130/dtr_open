import flightActions
class BlimpManeuvers():
    #contains all the defined flight actions blimp is setup to do.

    def __init__(self,comms):
        print("something here")
        self.comms = comms
        self.forward = self.initForward()
        self.three60 = self.init360()
        self.hover = self.initHover()

    def initForward(self,throttle = 0.5):
        forwardExitCriteria = flightActions.ExitCriteria()
        #forwardExitCriteria.add("timeClock",10)
        forwardExitCriteria.add("colorDetected",'green')

        forwardControls = flightActions.Controls()
        forwardControls.throttle = throttle
        #forwardControls.up = 1 #test only
        #forwardControls.yaw = 1 #test only

        forwardOrGreen = flightActions.FlightAction("Go forward until see green water bottle.",forwardControls,forwardExitCriteria,self.comms)
        return forwardOrGreen

    def init360(self,yaw = 0.5):
        three60orAprilTagExit = flightActions.ExitCriteria()
        #three60orAprilTagExit.add("timeClock",5) #need to figure out how long it takes to do 360...
        three60orAprilTagExit.add("isAprilTagDetected",True)
        three60orAprilTagCtrls = flightActions.Controls()
        three60orAprilTagCtrls.yaw = yaw

        three60orAprilTag = flightActions.FlightAction("360 or until see april tag.",three60orAprilTagCtrls,three60orAprilTagExit,self.comms)
        return three60orAprilTag

    def initHover(self,up = 0.5):
        #
        hoverExit = flightActions.ExitCriteria()
        #hoverExit.add("timeClock",5) #need to figure out how long it takes to do 360...
        hoverExit.add("irData",True)
        hoverCtrls = flightActions.Controls()
        hoverCtrls.up = up

        hover = flightActions.FlightAction("hover",hoverCtrls,hoverExit,self.comms)
        return hover