import sys
sys.path.append('C:\DroneRepos\DTRRepo\Blimp\OpenMV\support')

import time
import maneuvers
from maneuvers import ExitCriteria
from maneuvers import Maneuver
from maneuvers import Controls
import dataClasses



activeManuever = None

# setup forward motion control.
forwardExitCriteria = ExitCriteria()
forwardExitCriteria.add("timeClock",10)
#forwardExitCriteria.add("colorDetected",True)

forwardControls = Controls()
forwardControls.throttle = 0.5

forward = Maneuver("Go forward until see green water bottle.",forwardControls,forwardExitCriteria)


ctr = 0
while not forward.isExitCriteriaMet():    
    forward.execute()
    if(ctr == 3):
        dataClasses.data.colorDetected = True
    ctr = ctr + 1
    time.sleep(0.5)

print('test complete')

# setup 360 or until see april tag.
three60orAprilTagExit = ExitCriteria()
three60orAprilTagExit.add("timeClock",5) #need to figure out how long it takes to do 360...
three60orAprilTagExit.add("aprilTagDetected",True)
three60orAprilTagCtrls = Controls()
three60orAprilTagCtrls.yaw = 0.5

three60orAprilTag = Maneuver("360 or until see april tag.",three60orAprilTagCtrls,three60orAprilTagExit)


ctr = 0
while not three60orAprilTag.isExitCriteriaMet():    
    three60orAprilTag.execute()
    if(ctr == 3):
        dataClasses.data.aprilTagDetected = True
    ctr = ctr + 1
    time.sleep(0.5)

print('test complete')





