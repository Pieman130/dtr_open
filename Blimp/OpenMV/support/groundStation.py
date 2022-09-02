

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

        except:
            self.hw.turnOnNotConnectedToGndStationLight()
            print('cannot connect to server')
