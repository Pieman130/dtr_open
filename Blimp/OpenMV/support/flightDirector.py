import flightManeuvers
import dataClasses 
import logger

class FlightDirector:    
    ''' 
        Goal of the flight director:
            -read processed sensor data
            -manage the current flight maneuver
            -determines if another flight maneuver needs to be executed.
            -determine pid set values            
    '''
    def __init__(self,comms,hw):
        self.currentState = None # SET BY MISSION COMMANDER
        self.allowGroundStationCommands = True        
              
        self.requestedFirstManeuver = None
        self.requestedSecondManeuver = None
        self.blimpManeuvers = flightManeuvers.BlimpManeuvers(comms,hw)
        
        self.currentManeuver = self.blimpManeuvers.doNothing  
        

       # self.currentManeuver = self.blimpManeuvers
        #self.blimpManeuvers = flightManeuvers.BlimpManeuvers(comms)


    def getNextStep(self):
        
        if(self.currentState == None):
            self.currentManeuver = self.blimpManeuvers.doNothing 
            return
        else:

            logger.log.verbose(" FLIGHT DIRECTOR CURRENT MODE: " + self.currentState.description)     

            yawRate = 1
            # if(dataClasses.gndStationCmd.p_up != None):
                #   pass
                # logger.log.debugOnly("Pid Up.  P: " + str(dataClasses.gndStationCmd.p_up))
                    #logger.log.debugOnly("Pid Up.  I: " + str(dataClasses.gndStationCmd.i_up))
                    #logger.log.debugOnly("Pid Up.  D: " + str(dataClasses.gndStationCmd.d_up))

                    #logger.log.debugOnly("Pid Throttle.  P: " + str(dataClasses.gndStationCmd.p_throttle))
                    #logger.log.debugOnly("Pid Throttle.  I: " + str(dataClasses.gndStationCmd.i_throttle))
                    #logger.log.debugOnly("Pid Throttle.  D: " + str(dataClasses.gndStationCmd.d_throttle))

                    #logger.log.debugOnly("Pid Yaw.  P: " + str(dataClasses.gndStationCmd.p_yaw))
                    #logger.log.debugOnly("Pid Yaw.  I: " + str(dataClasses.gndStationCmd.i_yaw))
                    #logger.log.debugOnly("Pid Yaw.  D: " + str(dataClasses.gndStationCmd.d_yaw))

                    #logger.log.debugOnly("Scalar up: " + str(dataClasses.gndStationCmd.scalar_up))
                    #logger.log.debugOnly("Scalar yaw:  " + str(dataClasses.gndStationCmd.scalar_yaw))
                    #logger.log.debugOnly("Scalar throttle: " + str(dataClasses.gndStationCmd.scalar_throttle))


            if(self.currentState.description == 'manualTesting'):
                self.currentManeuver = self.blimpManeuvers.manualServerControl()
                self.currentManeuver.controls.up = dataClasses.gndStationCmd.manual_up
                self.currentManeuver.controls.throttle = dataClasses.gndStationCmd.manual_throttle
                self.currentManeuver.controls.yaw = dataClasses.gndStationCmd.manual_yaw
                self.currentManeuver.controls.servo = dataClasses.gndStationCmd.manual_servo
                
                
            elif(self.currentState.description == 'hover'):
                self.currentManeuver = self.blimpManeuvers.hover
                self.blimpManeuvers.hover.assistedAltitudeWebControlled()

            elif(self.currentState.description == 'hoverYaw'):
                self.currentManeuver = self.blimpManeuvers.hoverYaw
                self.blimpManeuvers.hoverYaw.assistedAltitudeWebControlled()
                self.blimpManeuvers.hoverYaw.execute_yaw_control(yawRate)

            
            elif(self.currentState.description == 'yaw'):   
                self.currentManeuver = self.blimpManeuvers.yaw             
                self.blimpManeuvers.yaw.execute_yaw_control(yawRate)
                
            

            elif(self.currentState.description == 'lookForBall'):
                self.currentManeuver = self.blimpManeuvers.three60
                
            #elif(self.currentState.description == 'moveToBall'):
            #      self.currentManeuver = self.blimpManeuvers.forward

            # elif(self.currentState.description == 'captureBall'):
            #     self.currentManeuver = self.blimpManeuvers.hover

            # elif(self.currentState.description == 'lookForGoal'):
            #     self.currentManeuver = self.blimpManeuvers.three60

            # elif(self.currentState.description == 'moveToGoal'):
            #     self.currentManeuver = self.blimpManeuvers.forward

            # elif(self.currentState.description == 'scoreGoal'):
            #     self.currentManeuver = self.blimpManeuvers.hover

            # elif(self.currentState.description == 'manualTesting'):


            # elif(self.currentState.description == 'automatedAssist'):

            #     self.currentManeuver.scalar_up = dataClasses.gndStationCmd.scalar_up
            #     self.currentManeuver.scalar_yaw = dataClasses.gndStationCmd.scalar_yaw
            #     self.currentManeuver.scalar_throttle = dataClasses.gndStationCmd.scalar_throttle

            #     self.currentManeuver.p_up = dataClasses.gndStationCmd.p_up
            #     self.currentManeuver.i_up = dataClasses.gndStationCmd.i_up
            #     self.currentManeuver.d_up = dataClasses.gndStationCmd.d_up

            #     self.currentManeuver.p_throttle = dataClasses.gndStationCmd.p_throttle
            #     self.currentManeuver.i_throttle = dataClasses.gndStationCmd.i_throttle
            #     self.currentManeuver.d_throttle = dataClasses.gndStationCmd.d_throttle

            #     self.currentManeuver.p_yaw = dataClasses.gndStationCmd.p_yaw
            #     self.currentManeuver.i_yaw = dataClasses.gndStationCmd.i_yaw
            #     self.currentManeuver.d_yaw = dataClasses.gndStationCmd.d_yaw
            

    def executeNextStep(self): # to be defined by determine next step
        self.currentManeuver.execute() 
        #pass

       # if(self.currentManeuver.description == "test"):

        #self.blimpManeuvers.hover.execute()
        #           

