import urequests

def getServerAddress(addr: str, api: str) -> str:
    return 'http://{}:1111/{}'.format(addr, api)

def sendStatusMessage(ipAddress: str, colorDetected: str):
    print('in print status message')
    data= '{"cameraDetectionStr":"' + colorDetected + '"}'
    print(data)
    #r = urequests.request('POST',fullAddress,data )
    headers = {'Content-Type': 'application/json'}

    fullAddress = getServerAddress(ipAddress,'/debug/status')
    print(fullAddress)
    #a = uping.ping(GROUND_STATION_IP);
    try:
        r = urequests.post(fullAddress,data = data,headers = headers)
        print('status to server success!')
    except:
        print('cannot connect to server')
