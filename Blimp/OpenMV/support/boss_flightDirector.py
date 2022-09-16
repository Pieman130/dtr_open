
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
        #self.currentState = lookForBall
        self.currentManeuver = "test"

        self.requestedFirstManeuver = None
        self.requestedSecondManeuver = None

        #self.blimpManeuvers = flightManeuvers.BlimpManeuvers(comms)

  

    def getNextStep(self):
        pass

    def executeNextStep(self):
        pass

