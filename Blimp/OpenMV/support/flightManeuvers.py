
## maneuvers
forwardExitCriteria = ExitCriteria()
#forwardExitCriteria.add("timeClock",10)
forwardExitCriteria.add("colorDetected",'green')

forwardControls = Controls()
forwardControls.throttle = 0.5
#forwardControls.up = 1 #test only
#forwardControls.yaw = 1 #test only

forwardOrGreen = Maneuver("Go forward until see green water bottle.",forwardControls,forwardExitCriteria)

##
three60orAprilTagExit = ExitCriteria()
#three60orAprilTagExit.add("timeClock",5) #need to figure out how long it takes to do 360...
three60orAprilTagExit.add("isAprilTagDetected",True)
three60orAprilTagCtrls = Controls()
three60orAprilTagCtrls.yaw = 0.5

three60orAprilTag = Maneuver("360 or until see april tag.",three60orAprilTagCtrls,three60orAprilTagExit)

#
hoverExit = ExitCriteria()
#hoverExit.add("timeClock",5) #need to figure out how long it takes to do 360...
hoverExit.add("irData",True)
hoverCtrls = Controls()
hoverCtrls.up = 0.5

hover = Maneuver("hover",hoverCtrls,hoverExit)