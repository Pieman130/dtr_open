class ConnectionInfo:
    def __init__(self):
        self.ssid = 'DTR_team_a'
        self.key = 'GoBigRed'
        self.ip = '192.168.1.100'

wifiInfo = ConnectionInfo()

import urequests
import network
import dataClasses 

def initialize():
    global wifiInfo
    wlan = network.WINC()
    print(wifiInfo)
    wlan.connect(wifiInfo.ssid, wifiInfo.key)
    print(wlan.ifconfig())

def getServerAddress(addr: str, api: str) -> str:
    return 'http://{}:1111/{}'.format(addr, api)

def sendStatusMessage():
    global wifiInfo    
    
    print('in print status message')
    data = '{"cameraDetectionStr":"' + dataClasses.data.colorDetected + '"'
    ir1_0str = str(int(dataClasses.data.irData))
    data = data + ',"isIrSensorDetection":"' + ir1_0str + '"}'
    print(data)
    #r = urequests.request('POST',fullAddress,data )
    headers = {'Content-Type': 'application/json'}

    fullAddress = getServerAddress(wifiInfo.ip,'debug/status')
    print("about to post data to: " + fullAddress)

    #a = uping.ping(wifiInfo.ip) # - EINVAL error.. ? why
    
    try:
        r = urequests.post(fullAddress,data = data,headers = headers)
                
        print('status to server success! received:')              
        jsonList = r.json()
        jsonDict = jsonList[0]                    
                
        dataClasses.gndStationCmd.maneuverDescription = jsonDict['maneuverDescription']
        dataClasses.gndStationCmd.baseUpVal = jsonDict['baseUpVal']
        dataClasses.gndStationCmd.duration = jsonDict['duration']
        

    except:
       print('cannot connect to server')
