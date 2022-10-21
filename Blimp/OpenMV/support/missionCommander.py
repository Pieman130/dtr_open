import logger
import dataClasses 
import processing

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

startup = SystemState("startup","none","none")
lookForBall = SystemState("lookForBall",TARGET_BALL,ACTION_LOOK)
moveToBall = SystemState("moveToBall",TARGET_BALL,ACTION_MOVE)
captureBall = SystemState("captureBall", TARGET_BALL,ACTION_CAPTURE)
lookForGoal = SystemState("lookForGoal",TARGET_GOAL,ACTION_LOOK)
moveToGoal = SystemState("moveToGoal", TARGET_GOAL,ACTION_MOVE)
scoreGoal = SystemState("scoreGoal",TARGET_GOAL,ACTION_RELEASE)
manualTesting = SystemState("manualTesting",TARGET_GOAL,ACTION_RELEASE)
automatedAssist = SystemState("automatedAssist",TARGET_GOAL,ACTION_RELEASE)


    
CONTROL_AUTHORITY_AUTO = "autonomous"
CONTROL_AUTHORITY_AUTO_ASSISTED = "auto-assisted"
CONTROL_AUTHORITY_MANUAL_WEB = "manualWeb"
CONTROL_AUTHORITY_MANUAL_REMOTE = "manualRemote"
class MissionCommander:   
    '''    Mission commander:
           Goal: 
            -Determine control authority.
            -Manages the state of the system.  Look for Ball, move to Ball etc.
                -read processed sensor values and determine if the state needs to change        
                -pass the value of the current state to the flight director.    
    '''
    def __init__(self,flightDirector):
        self.currentState = startup
        self.flightDirector = flightDirector

    def updateState(self): #to be redefined by which control authority is selected
        pass

    def determineControlAuthority(self):

        processing.parseSensorData()
        processing.parseRCSwitchPositions()

        if dataClasses.data.sw_door_control is not None:
            logger.log.verbose("DoorSwitch: " + dataClasses.data.sw_door_control)
        if dataClasses.data.sw_flight_mode is not None:
            logger.log.verbose("FlightMode: " + dataClasses.data.sw_flight_mode)


        if (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_AUTO):   
            logger.log.verbose("CONTROL AUTHORITY: Auto")                  
            self.updateState = self.updateStateAuto
            
        elif (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_AUTO_ASSISTED):
            logger.log.verbose("CONTROL AUTHORITY: Auto assisted")             
            self.updateState = self.updateStateAutoAssisted

        elif (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_MANUAL_WEB):
            logger.log.verbose("CONTROL AUTHORITY: Manual Web")
            self.updateState = self.updateStateManualWeb

        elif (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_MANUAL_REMOTE):
            logger.log.verbose("CONTROL AUTHORITY: Manual Remote")  
            self.updateState = self.updateStateManualRemote
        else:
            dataClasses.gndStationCmd.controlAuthority = CONTROL_AUTHORITY_AUTO
            self.updateState = self.updateStateAuto


        dataClasses.config.controlAuthority = dataClasses.gndStationCmd.controlAuthority
   

    def updateStateAutoAssisted(self):        
        requestedState = dataClasses.gndStationCmd.requestedState     

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


    def updateStateManualWeb(self):                
        logger.log.verbose("changed to manual testing")             
        self.flightDirector.currentState = manualTesting

    def updateStateAuto(self):  
          
        self.flightDirector.currentState = self.currentState    

    def updateStateManualRemote(self):
         
        self.flightDirector.currentState = self.currentState

    


    
