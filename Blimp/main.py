# Untitled - By: timothy.woodbridge - Fri May 20 2022

import sensor, image, time,network,urequests,json

SSID='DTR_team_a' # Network SSID
KEY='GoBigRed'  # Network key
GROUND_STATION_IP = '192.168.1.100'

def main() -> None:

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)

    fullAddress = getFullAddress(GROUND_STATION_IP, 'debug/status')

    # Init wlan module and connect to network
    wlan = network.WINC()
    wlan.connect(SSID, KEY) #, security=wlan.WPA_PSK)

    print(wlan.ifconfig())


    clock = time.clock()

    while(True):

        clock.tick()
        img = sensor.snapshot()
        sendStatusMessage(fullAddress)
        print('status message success!')
        time.sleep(1)

def sendStatusMessage(fullAddress: str):
    dataToSend = {'stateID': 1, 'message':'test'}
    r = urequests.request('POST',fullAddress,data = json.dumps(dataToSend).encode('utf-8') )

def getFullAddress(addr: str, api: str) -> str:
    return 'http://{}:4000/{}'.format(addr, api)

main()
