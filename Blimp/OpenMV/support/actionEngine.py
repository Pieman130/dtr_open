import dataClasses
import maneuvers
currentState = None
currentManeuver = None

ACTION_LOOK = "look"
ACTION_MOVE = "move"
ACTION_RELEASE = "release"
ACTION_CAPTURE = "capture"

TARGET_BALL = "ball"
TARGET_GOAL = "goal"

MODE_BLIND = "blind"
MODE_COARSE = "coarse"
MODE_FINE = "fine"
class StateEngine:
    def __init__(self):
        mode = ''
        exitCriteria = dataClasses.ProcessedData()
    def isTimeToExit(self):
        if self.exitCriteria == dataClasses.data:
            print("time to exit")

class SystemState:
    def __init__(self,description,target,action):
        self.description = description
        self.target = target
        self.action = action    



lookForBall = SystemState("Search for ball.",TARGET_BALL,ACTION_LOOK)
moveToBall = SystemState("Move to ball.",TARGET_BALL,ACTION_MOVE)
captureBall = SystemState("Capture the ball.", TARGET_BALL,ACTION_CAPTURE)
lookForGoal = SystemState("Search for goal.",TARGET_GOAL,ACTION_LOOK)
moveToGoal = SystemState("Move to goal.", TARGET_GOAL,ACTION_MOVE)
scoreGoal = SystemState("Score goal.",TARGET_GOAL,ACTION_RELEASE)


    
def initialize():
    global currentState
    currentState = lookForBall

def updateState():
    # do I switch system states?
    print('update state called')

def getNextStep(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h 
    global currentManeuver
    dataClasses.gndStationCmd.print()
    #dataClasses.gndStationCmd.maneuverDescription

    print(" action engine! ir data: " + str(dataClasses.data.irData))
    print(" action engine! img: " + str(dataClasses.data.colorDetected))
    output = 0
    print("get next step")

    
    print(dataClasses.data.aprilTagFound.foundIt)
    print("rotation: " + str(dataClasses.data.aprilTagFound.rotation))

    print("GROUND STATION MANEUVER: " + dataClasses.gndStationCmd.maneuverDescription)

    if not currentManeuver == None:
        if currentManeuver.isExitCriteriaMet():
            currentManeuver = None

    if currentManeuver == None:        
        currentManeuver = getManeuver(dataClasses.gndStationCmd.maneuverDescription)
        currentManeuver.reset()

    dataClasses.gndStationCmd.maneuverDescription
    dataClasses.gndStationCmd.baseUpVal
    dataClasses.gndStationCmd.duration

    #moveForwardFull()

    return output

def getManeuver(desc):
    if (desc == 'forward'):
        print("NEXT MANEUVER - FORWARD")
        nextManeuver = maneuvers.forwardOrGreen
    elif (desc == '360'):
        print("NEXT MANEUVER - 360")
        nextManeuver = maneuvers.three60orAprilTag
    else:
        print("NEXT MANEUVER - HOVER")
        nextManeuver = maneuvers.hover

    return nextManeuver

def executeNextStep():
    global currentManeuver
    currentManeuver.execute()
    print("do nothing")
  #  global msgToSend
   # output = 0
  #  print("execute next step")

    
    ## need to put this  somewhere...
    
   # minValue = 1100 #backwards
   # midValue = 1500 #0
   # fullValue = 1900 #full forward

    # mavlink_messages 
    # #2 = lift
    # #3 = throttle
    # #4 = up

    
   # ch = (0,fullValue,fullValue,fullValue,0,0,0,0)

    #ctr = ctr + 1
    #msgToSend = mavlink_messages.mvlink_ch_overide(ctr,ch)
    
    
    #pixracer.write(msgToSend)
