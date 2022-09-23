import flightManeuvers
import dataClasses 

class FlightDirector:    
    ''' 
        Goal of the flight director:
            -read processed sensor data
            -manage the current flight maneuver
            -determines if another flight maneuver needs to be executed.
            -determine pid set values            
    '''
    def __init__(self,comms):
        self.allowGroundStationCommands = True        
        self.currentManeuver = None
        self.currentState = None

        self.requestedFirstManeuver = None
        self.requestedSecondManeuver = None
        self.blimpManeuvers = flightManeuvers.BlimpManeuvers(comms)
        #self.blimpManeuvers = flightManeuvers.BlimpManeuvers(comms)

  

    def getNextStep(self):
        print(" FLIGHT DIRECTOR CURRENT MODE: " + self.currentState.description)     

        if(self.currentState.description == 'lookForBall'):
            self.currentManeuver = self.blimpManeuvers.three60
            
        elif(self.currentState.description == 'moveToBall'):
             self.currentManeuver = self.blimpManeuvers.forward

        elif(self.currentState.description == 'captureBall'):
            self.currentManeuver = self.blimpManeuvers.hover

        elif(self.currentState.description == 'lookForGoal'):
            self.currentManeuver = self.blimpManeuvers.three60

        elif(self.currentState.description == 'moveToGoal'):
            self.currentManeuver = self.blimpManeuvers.forward

        elif(self.currentState.description == 'scoreGoal'):
            self.currentManeuver = self.blimpManeuvers.hover

        elif(self.currentState.description == 'manualTesting'):
            self.currentManeuver = self.blimpManeuvers.manualServerControl()
            self.currentManeuver.controls.up = dataClasses.gndStationCmd.manual_up
            self.currentManeuver.controls.throttle = dataClasses.gndStationCmd.manual_throttle
            self.currentManeuver.controls.yaw = dataClasses.gndStationCmd.manual_yaw
            self.currentManeuver.controls.servo = dataClasses.gndStationCmd.manual_servo


            print('test')
            #dataClasses

        elif(self.currentState.description == 'automatedAssist'):

            self.currentManeuver.scalar_up = dataClasses.gndStationCmd.scalar_up
            self.currentManeuver.scalar_yaw = dataClasses.gndStationCmd.scalar_yaw
            self.currentManeuver.scalar_throttle = dataClasses.gndStationCmd.scalar_throttle

            self.currentManeuver.p_up = dataClasses.gndStationCmd.p_up
            self.currentManeuver.i_up = dataClasses.gndStationCmd.i_up
            self.currentManeuver.d_up = dataClasses.gndStationCmd.d_up

            self.currentManeuver.p_throttle = dataClasses.gndStationCmd.p_throttle
            self.currentManeuver.i_throttle = dataClasses.gndStationCmd.i_throttle
            self.currentManeuver.d_throttle = dataClasses.gndStationCmd.d_throttle

            self.currentManeuver.p_yaw = dataClasses.gndStationCmd.p_yaw
            self.currentManeuver.i_yaw = dataClasses.gndStationCmd.i_yaw
            self.currentManeuver.d_yaw = dataClasses.gndStationCmd.d_yaw
            

    def executeNextStep(self):
       # if(self.currentManeuver.description == "test"):
        self.currentManeuver.execute()            

