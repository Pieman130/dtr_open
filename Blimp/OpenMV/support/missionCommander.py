import logger
import dataClasses 

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

class SystemState:
    def __init__(self,description,target,action):
        self.description = description
        self.target = target
        self.action = action    

lookForBall = SystemState("lookForBall",TARGET_BALL,ACTION_LOOK)
moveToBall = SystemState("moveToBall",TARGET_BALL,ACTION_MOVE)
captureBall = SystemState("captureBall", TARGET_BALL,ACTION_CAPTURE)
lookForGoal = SystemState("lookForGoal",TARGET_GOAL,ACTION_LOOK)
moveToGoal = SystemState("moveToGoal", TARGET_GOAL,ACTION_MOVE)
scoreGoal = SystemState("scoreGoal",TARGET_GOAL,ACTION_RELEASE)
manualTesting = SystemState("manualTesting",TARGET_GOAL,ACTION_RELEASE)
automatedAssist = SystemState("automatedAssist",TARGET_GOAL,ACTION_RELEASE)

    
class MissionCommander:   
    '''    Mission commander:
           Goal: 
            -Manages the state
            -read processed sensor values and determine if the state needs to change            
    '''
    def __init__(self,flightDirector):
        self.currentState = lookForBall # default startup state
        self.flightDirector = flightDirector

    def updateState(self):  
                   
        requestedState = dataClasses.gndStationCmd.requestedState   

        if(self.currentState.description == requestedState):
            pass #do nothing.
            
        else:
            if(requestedState == lookForBall.description):
                logger.log.verbose("changed to look for ball")
                self.currentState = lookForBall
                

            elif(requestedState == moveToBall.description):
                self.currentState = moveToBall
                logger.log.verbose("changed to moveToBall")

            elif(requestedState == captureBall.description):
                self.currentState = captureBall
                logger.log.verbose("changed to captureBall")

            elif(requestedState == lookForGoal.description):
                self.currentState = lookForGoal
                logger.log.verbose("changed to lookForGoal")

            elif(requestedState == moveToGoal.description):
                self.currentState = moveToGoal
                logger.log.verbose("changed to moveToGoal")

            elif(requestedState == scoreGoal.description):
                self.currentState = scoreGoal
                logger.log.verbose("changed to scoreGoal")


            elif(requestedState == manualTesting.description):
                self.currentState = manualTesting
                logger.log.verbose("changed to scoreGoal")


            elif(requestedState == automatedAssist.description):
                self.currentState = automatedAssist
                logger.log.verbose("changed to scoreGoal")                

            self.flightDirector.currentState = self.currentState
    
