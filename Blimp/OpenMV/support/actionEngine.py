import dataClasses
import flightManeuvers


ACTION_LOOK = "look"
ACTION_MOVE = "move"
ACTION_RELEASE = "release"
ACTION_CAPTURE = "capture"

TARGET_BALL = "ball"
TARGET_GOAL = "goal"

MODE_BLIND = "blind"
MODE_COARSE = "coarse"
MODE_FINE = "fine"

STOP_CTR_MAX = 15
stopCtr = 0

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

class ActionEngine:
    def __init__(self,comms):
        self.currentState = lookForBall
        self.currentManeuver = None
        self.blimpManeuvers = flightManeuvers.BlimpManeuvers(comms)

    def updateState(self):
        # do I switch system states?
        print('update state called')

    def getNextStep(self): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h 
        global currentManeuver
        global stopCtr
        global STOP_CTR_MAX

        dataClasses.gndStationCmd.print()
        #dataClasses.gndStationCmd.maneuverDescription

        print(" action engine! ir data: " + str(dataClasses.data.irData))
        print(" action engine! img: " + str(dataClasses.data.colorDetected))
        output = 0
        print("get next step")

        
        print(dataClasses.data.aprilTagFound.foundIt)
        print("rotation: " + str(dataClasses.data.aprilTagFound.rotation))

        print("GROUND STATION MANEUVER: " + dataClasses.gndStationCmd.maneuverDescription)

        if not self.currentManeuver == None:
            if stopCtr>STOP_CTR_MAX: 
                stopCtr = 0
                currentManeuver = None

        if self.currentManeuver == None:        
            currentManeuver = self.getManeuver(dataClasses.gndStationCmd.maneuverDescription)
            currentManeuver.reset()

    # dataClasses.gndStationCmd.maneuverDescription
    # dataClasses.gndStationCmd.baseUpVal
    # dataClasses.gndStationCmd.duration

        #moveForwardFull()

        return output

    def getManeuver(self,desc):
        global blimpManeuvers

        if (desc == 'forward'):
            print("NEXT MANEUVER - FORWARD")
            

            nextManeuver = self.blimpManeuvers.forward
        elif (desc == '360'):
            print("NEXT MANEUVER - 360")
            nextManeuver = self.blimpManeuvers.three60
        else:
            print("NEXT MANEUVER - HOVER")
            nextManeuver = self.blimpManeuvers.hover

        return nextManeuver

    def executeNextStep():
        global stopCtr
        global currentManeuver
        if currentManeuver.isExitCriteriaMet():
            print("NO OP")
            currentManeuver.sendNoop()            
            stopCtr = stopCtr + 1
            print("stop ctr: " + str(stopCtr))
        else:
            print("EXECUTE")
            currentManeuver.execute()
            
     
