import flightActions
class BlimpManeuvers():
    #contains all the defined flight actions blimp is setup to do.

    def __init__(self,comms,hw):        
        self.hw = hw
        self.comms = comms
        self.forward = self.initForward()
        self.three60 = self.init360()
        self.hover = self.initHover()     
        self.doNothing = self.initDoNothing()

    def initDoNothing(self):
        exitCriteria = flightActions.ExitCriteria()
        controls = flightActions.Controls()

        doNothing = flightActions.FlightAction("Do nothing.",controls,exitCriteria,self.comms,self.hw)
        doNothing.execute = doNothing.executeNoop
        return doNothing

    def initForward(self,throttle = 0.5):
        forwardExitCriteria = flightActions.ExitCriteria()
        #forwardExitCriteria.add("timeClock",10)
        forwardExitCriteria.add("colorDetected",'green')

        forwardControls = flightActions.Controls()
        forwardControls.throttle = throttle
        #forwardControls.up = 1 #test only
        #forwardControls.yaw = 1 #test only

        forwardOrGreen = flightActions.FlightAction("Go forward until see green water bottle.",forwardControls,forwardExitCriteria,self.comms,self.hw)
        return forwardOrGreen

    def init360(self,yaw = 0.5):
        three60orAprilTagExit = flightActions.ExitCriteria()
        #three60orAprilTagExit.add("timeClock",5) #need to figure out how long it takes to do 360...
        three60orAprilTagExit.add("isAprilTagDetected",True)
        three60orAprilTagCtrls = flightActions.Controls()
        three60orAprilTagCtrls.yaw = yaw

        three60orAprilTag = flightActions.FlightAction("360 or until see april tag.",three60orAprilTagCtrls,three60orAprilTagExit,self.comms,self.hw)
        return three60orAprilTag

    def initHover(self,up = 0.5):
        #
        hoverExit = flightActions.ExitCriteria()
        #hoverExit.add("timeClock",5) #need to figure out how long it takes to do 360...
        hoverExit.add("irData",True)
        hoverCtrls = flightActions.Controls()
        hoverCtrls.up = up

        hover = flightActions.FlightAction("hover",hoverCtrls,hoverExit,self.comms,self.hw)
        return hover

    def manualServerControl(self):
        manualExit = flightActions.ExitCriteria()
        manualCtrl = flightActions.Controls()
        #manualCtrl.up = up
       # manualCtrl.throttle = throttle
        #manualCtrl.yaw = yaw

        manual = flightActions.FlightAction("manual",manualCtrl,manualExit,self.comms,self.hw)
        return manual

    def test(self):
        testExit = flightActions.ExitCriteria()
        testCtrl = flightActions.Controls()
        #manualCtrl.up = up
       # manualCtrl.throttle = throttle
        #manualCtrl.yaw = yaw

        manual = flightActions.FlightAction("test",testCtrl,testExit,self.comms,self.hw)
        return manual        