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
hover = SystemState("hover","none","none")
hoverYaw = SystemState("hoverYaw","none","none")
yaw = SystemState("yaw","none","none")

autonomous = SystemState("autonomous","none","none")
manualTesting = SystemState("manualTesting","none","none") # direct control of motors
rcControl = SystemState("rcRemote","none","none") # direct control of motors


lookForBall = SystemState("lookForBall",TARGET_BALL,ACTION_LOOK)
moveToBall = SystemState("moveToBall",TARGET_BALL,ACTION_MOVE)
captureBall = SystemState("captureBall", TARGET_BALL,ACTION_CAPTURE)
lookForGoal = SystemState("lookForGoal",TARGET_GOAL,ACTION_LOOK)
moveToGoal = SystemState("moveToGoal", TARGET_GOAL,ACTION_MOVE)
scoreGoal = SystemState("scoreGoal",TARGET_GOAL,ACTION_RELEASE)




CONTROL_AUTHORITY_AUTO = "auto"
CONTROL_AUTHORITY_RC_REMOTE_CONTROL = "manual"    
CONTROL_AUTHORITY_AUTO_ASSISTED = "assisted"


WEB_ASSISTED_STATE_TEST = "auto-assisted"
WEB_ASSISTED_STATE_AUTO = "autonomous"
WEB_ASSISTED_STATE_MANUAL = "manualWeb"

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
        #logger.log.verbose('sw flight mode: ' + str(dataClasses.config.controlAuthority ))
        #logger.log.verbose('sw door control: ' + str(dataClasses.data.sw_door_control))

        logger.log.verbose("FLIGHT MODE:")
        logger.log.verbose(dataClasses.config.controlAuthority)

        logger.log.debugOnly('flight mode: ' + dataClasses.config.controlAuthority)

       # dataClasses.config.controlAuthority = CONTROL_AUTHORITY_RC_REMOTE_CONTROL
             
        
        if(dataClasses.config.controlAuthority == dataClasses.constants.CONTROL_AUTHORITY_AUTO):
              self.updateState = self.updateStateAuto
              
        else:
            self.updateState = self.updateStateManualRemote
            

        
        # if( (dataClasses.config.controlAuthority == CONTROL_AUTHORITY_RC_REMOTE_CONTROL) or
        #      (dataClasses.gndStationCmd.controlAuthority == CONTROL_AUTHORITY_RC_REMOTE_CONTROL) ):
        #     self.updateState = self.updateStateManualRemote        

        # elif(dataClasses.config.controlAuthority == CONTROL_AUTHORITY_AUTO or
        #     dataClasses.gndStationCmd.controlAuthority == WEB_ASSISTED_STATE_AUTO):
        #      self.updateState = self.updateStateAuto        

        # elif(dataClasses.config.controlAuthority == CONTROL_AUTHORITY_AUTO_ASSISTED):            
        #     if (dataClasses.gndStationCmd.controlAuthority == WEB_ASSISTED_STATE_TEST):
        #         logger.log.verbose("CONTROL AUTHORITY: Auto assisted")             
        #         self.updateState = self.updateStateAutoAssisted
        #         webAuthority = 'web auto-assisted'

        #     elif (dataClasses.gndStationCmd.controlAuthority == WEB_ASSISTED_STATE_MANUAL):
        #         logger.log.verbose("CONTROL AUTHORITY: Manual Web")
        #         self.updateState = self.updateStateManualWeb
        #         webAuthority = 'web manual'

        #     else:
        #         logger.log.verbose("CONTROL AUTHORITY: Manual Web")
        #         self.updateState = self.updateStateManualWeb
        #         webAuthority = 'web manual'


        logger.log.verbose('CONTROL AUTHORITY: ' + dataClasses.config.controlAuthority)
        
   

    def updateStateAutoAssisted(self):                              
        requestedState = dataClasses.gndStationCmd.requestedState     

        if(requestedState == hover.description):
            self.currentState = hover

        elif(requestedState == hoverYaw.description):
            self.currentState = hoverYaw


        elif(requestedState == yaw.description):
            self.currentState = yaw
        
        else:
            self.currentState = startup

        
            
       # elif(requestedState == lookForBall.description):
        #    logger.log.verbose("changed to look for ball")
         #   self.currentState = lookForBall                

        #elif(requestedState == moveToBall.description):
         #   self.currentState = moveToBall
          #  logger.log.verbose("changed to moveToBall")

        #elif(requestedState == captureBall.description):
         #   self.currentState = captureBall
          #  logger.log.verbose("changed to captureBall")

       # elif(requestedState == lookForGoal.description):
        #    self.currentState = lookForGoal
         #   logger.log.verbose("changed to lookForGoal")

        #elif(requestedState == moveToGoal.description):
         #   self.currentState = moveToGoal
          #  logger.log.verbose("changed to moveToGoal")

        #elif(requestedState == scoreGoal.description):
         #   self.currentState = scoreGoal
          #  logger.log.verbose("changed to scoreGoal")

        self.flightDirector.currentState = self.currentState    


    def updateStateManualWeb(self):                
        logger.log.verbose("changed to manual testing")    
        self.currentState = manualTesting         
        self.flightDirector.currentState = manualTesting

    def updateStateAuto(self):           
        self.currentState = autonomous         
        self.flightDirector.currentState = autonomous  

    def updateStateManualRemote(self):
        self.currentState = rcControl     
        self.flightDirector.currentState = rcControl # self.currentState

    


    
