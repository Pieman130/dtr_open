
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

lookForBall = SystemState("Search for ball.",TARGET_BALL,ACTION_LOOK)
moveToBall = SystemState("Move to ball.",TARGET_BALL,ACTION_MOVE)
captureBall = SystemState("Capture the ball.", TARGET_BALL,ACTION_CAPTURE)
lookForGoal = SystemState("Search for goal.",TARGET_GOAL,ACTION_LOOK)
moveToGoal = SystemState("Move to goal.", TARGET_GOAL,ACTION_MOVE)
scoreGoal = SystemState("Score goal.",TARGET_GOAL,ACTION_RELEASE)

    
class MissionCommander:   
    '''    Mission commander:
           Goal: 
            -Manages the state
            -read processed sensor values and determine if the state needs to change
            

    '''
    def __init__(self):
        self.currentState = lookForBall # default startup state

    def updateState(self):
        pass

    
