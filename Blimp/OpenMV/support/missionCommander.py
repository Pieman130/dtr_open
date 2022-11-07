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
hover = SystemState("hover","nothing","nothing")
hoverYaw = SystemState("hoverYaw","nothing","nothing")
yaw = SystemState("yaw","nothing","nothing")

lookForBall = SystemState("lookForBall",TARGET_BALL,ACTION_LOOK)
moveToBall = SystemState("moveToBall",TARGET_BALL,ACTION_MOVE)
captureBall = SystemState("captureBall", TARGET_BALL,ACTION_CAPTURE)
lookForGoal = SystemState("lookForGoal",TARGET_GOAL,ACTION_LOOK)
moveToGoal = SystemState("moveToGoal", TARGET_GOAL,ACTION_MOVE)
scoreGoal = SystemState("scoreGoal",TARGET_GOAL,ACTION_RELEASE)

manualTesting = SystemState("manualTesting",TARGET_GOAL,ACTION_RELEASE) # direct control of motors
rcControl = SystemState("manual","none","none") # direct control of motors


    
CONTROL_AUTHORITY_AUTO = "autonomous"
CONTROL_AUTHORITY_AUTO_ASSISTED = "auto-assisted"
CONTROL_AUTHORITY_MANUAL_WEB = "manualWeb"
CONTROL_AUTHORITY_MANUAL_REMOTE = "manualRemote"
CONTROL_AUTHORITY_RC_REMOTE_CONTROL = "manual"
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
        processing.parseRCSwitchPositions()

        
        #logger.log.verbose('sw flight mode: ' + str(dataClasses.rawData.rc_sw_flt_mode))
        #logger.log.verbose('sw flight mode: ' + str(dataClasses.data.sw_flight_mode ))
        #logger.log.verbose('sw door control: ' + str(dataClasses.data.sw_door_control))

        logger.log.verbose("FLIGHT MODE:")
        logger.log.verbose(dataClasses.data.sw_flight_mode)

       # dataClasses.data.sw_flight_mode = CONTROL_AUTHORITY_RC_REMOTE_CONTROL
        controlAuthority = ''

        if(dataClasses.data.sw_flight_mode == CONTROL_AUTHORITY_RC_REMOTE_CONTROL):
            self.updateState = self.updateStateManualRemote
            controlAuthority = 'rc remote control'

        elif(dataClasses.data.sw_flight_mode == 'auto'):
             self.updateState = self.updateStateAuto
             controlAuthority = 'auto'

        elif(dataClasses.data.sw_flight_mode == 'assisted'):
            if (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_AUTO_ASSISTED):
                logger.log.verbose("CONTROL AUTHORITY: Auto assisted")             
                self.updateState = self.updateStateAutoAssisted
                controlAuthority = dataClasses.gndStationCmd.controlAuthority

            elif (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_MANUAL_WEB):
                logger.log.verbose("CONTROL AUTHORITY: Manual Web")
                self.updateState = self.updateStateManualWeb
                controlAuthority = dataClasses.gndStationCmd.controlAuthority

            else:
                dataClasses.gndStationCmd.controlAuthority = CONTROL_AUTHORITY_AUTO
                self.updateState = self.updateStateAuto
                controlAuthority = 'auto'
            

       # if dataClasses.data.sw_door_control is not None:
       #     logger.log.verbose("DoorSwitch: " + dataClasses.data.sw_door_control)
       # if dataClasses.data.sw_flight_mode is not None:
       #     logger.log.verbose("FlightMode: " + dataClasses.data.sw_flight_mode)


       # if (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_AUTO):   
        #    logger.log.verbose("CONTROL AUTHORITY: Auto")                  
         #   self.updateState = self.updateStateAuto
            
        

        #elif (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_MANUAL_REMOTE):
         #   logger.log.verbose("CONTROL AUTHORITY: Manual Remote")  
          #  self.updateState = self.updateStateManualRemote
        #else:
           


        dataClasses.config.controlAuthority = controlAuthority
   

    def updateStateAutoAssisted(self):        
        requestedState = dataClasses.gndStationCmd.requestedState     

        if(requestedState == hover.description):
            self.currentState = hover

        elif(requestedState == hoverYaw.description):
            self.currentState = hoverYaw

        elif(requestedState == yaw.description):
            self.currentState = yaw
            
        elif(requestedState == lookForBall.description):
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

        self.flightDirector.currentState = self.currentState    


    def updateStateManualWeb(self):                
        logger.log.verbose("changed to manual testing")             
        self.flightDirector.currentState = manualTesting

    def updateStateAuto(self):  
          
        self.flightDirector.currentState = self.currentState    

    def updateStateManualRemote(self):
         
        self.flightDirector.currentState = rcControl # self.currentState

    


    
