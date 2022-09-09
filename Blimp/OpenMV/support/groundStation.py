import dataClasses 

class GroundStation:
    def __init__(self,comms,hw):
        self.wifi = comms.wifi
        self.hw = hw

    def sendStatusMessage(self):
        global wifiInfo    
        
        print('in print status message')
        data = '{"cameraDetectionStr":"' + dataClasses.data.colorDetected + '"'
        ir1_0str = str(int(dataClasses.data.irData))
        data = data + ',"isIrSensorDetection":"' + ir1_0str + '"}'
        print(data)
        #r = urequests.request('POST',fullAddress,data )
        headers = {'Content-Type': 'application/json'}

        fullAddress = self.wifi.getFullAddress(self.wifi.ip,'debug/status')        

        print("about to post data to: " + fullAddress)

        #a = uping.ping(wifiInfo.ip) # - EINVAL error.. ? why
        
        try:
            r = self.wifi.post(fullAddress,data = data,headers = headers)            
                    
            print('status to server success! received:')              
            jsonList = r.json()
            jsonDict = jsonList[0]                    
                    

            self.hw.turnOnConnectedToGndStationLight()
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

        except:
            self.hw.turnOnNotConnectedToGndStationLight()
            print('cannot connect to server')
