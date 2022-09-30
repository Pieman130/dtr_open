import dataClasses 
import logger

class GroundStation:
    def __init__(self,comms,hw):
        self.wifi = comms.wifi
        self.hw = hw

    def sendStatusMessage(self,missionCommander,flightDirector):
        global wifiInfo    
        
        logger.log.verbose('in print status message')
        data = '{"cameraDetectionStr":"' + dataClasses.data.colorDetected + '"'
        ir1_0str = str(int(dataClasses.data.irData))

        data = data + ',"isIrSensorDetection":"' + ir1_0str + '"'

        data = data + ',"lidarDistance_ft":"' + str(dataClasses.data.lidarDistance_ft) + '"'

        data = data + ',"state_description":"' + missionCommander.currentState.description + '"'
        data = data + ',"state_target":"' + missionCommander.currentState.target + '"'
        data = data + ',"state_action":"' + missionCommander.currentState.action + '"'
        
        data = data + ',"currentManeuver":"' + flightDirector.currentManeuver.description + '"'

        data = data +  '}'

        logger.log.verbose(data)
        #r = urequests.request('POST',fullAddress,data )
        headers = {'Content-Type': 'application/json'}

        fullAddress = self.wifi.getFullAddress(self.wifi.ip,'debug/status')        

        logger.log.verbose("about to post data to: " + fullAddress)

        #a = uping.ping(wifiInfo.ip) # - EINVAL error.. ? why
        
        try:
            r = self.wifi.post(fullAddress,data = data,headers = headers)            
                    
            logger.log.verbose('status to server success! received:')              
            jsonList = r.json()
            jsonDict = jsonList[0]                    
                    

            self.hw.turnOnConnectedToGndStationLight()
            dataClasses.gndStationCmd.requestedState = jsonDict['requestedState']
            dataClasses.gndStationCmd.firstManeuver = jsonDict['firstManeuver']
            dataClasses.gndStationCmd.secondManeuver = jsonDict['secondManeuver']
            dataClasses.gndStationCmd.baseUpVal = jsonDict['baseUpVal']
            dataClasses.gndStationCmd.duration = jsonDict['duration']

            dataClasses.gndStationCmd.p_up = jsonDict['p_up']
            dataClasses.gndStationCmd.i_up = jsonDict['i_up']
            dataClasses.gndStationCmd.d_up = jsonDict['d_up']

            dataClasses.gndStationCmd.p_throttle = jsonDict['p_throttle']
            dataClasses.gndStationCmd.i_throttle = jsonDict['i_throttle']
            dataClasses.gndStationCmd.d_throttle = jsonDict['d_throttle']
            
            dataClasses.gndStationCmd.p_yaw = jsonDict['p_yaw']
            dataClasses.gndStationCmd.i_yaw = jsonDict['i_yaw']
            dataClasses.gndStationCmd.d_yaw = jsonDict['d_yaw']            
            dataClasses.gndStationCmd.requestedState = jsonDict['requestedState'] 

            dataClasses.gndStationCmd.manual_up = jsonDict['manual_up'] 
            dataClasses.gndStationCmd.manual_throttle = jsonDict['manual_throttle'] 
            dataClasses.gndStationCmd.manual_yaw = jsonDict['manual_yaw'] 
            dataClasses.gndStationCmd.manual_servo = jsonDict['manual_servo'] 

            dataClasses.gndStationCmd.scalar_up = jsonDict['scalar_up'] 
            dataClasses.gndStationCmd.scalar_yaw = jsonDict['scalar_yaw'] 
            dataClasses.gndStationCmd.scalar_throttle = jsonDict['scalar_throttle'] 


        except:
            self.hw.turnOnNotConnectedToGndStationLight()
            logger.log.warning('cannot connect to server')
