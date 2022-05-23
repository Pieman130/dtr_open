# Untitled - By: timothy.woodbridge - Fri May 20 2022

import sensor, image, time,network,urequests,json,math

threshold_index = 1 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0),
              (50, 100,-20,20, 30, 100)] # generic_yellow_thresholds] # generic_blue_thresholds


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
    wlan.connect(SSID, KEY)

    print(wlan.ifconfig())


    clock = time.clock()

    while(True):

        clock.tick()
        img = sensor.snapshot()

        print('status message success!')
        time.sleep(1)
        colorDetected = colorDetectedByCamera(img)
        sendStatusMessage(fullAddress,colorDetected)
        print(colorDetected)

def sendStatusMessage(fullAddress: str, colorDetected: str):
    #data = '{"value": "50"}'
    data= '{"cameraDetectionStr":"' + colorDetected + '"}'
    print(data)
    #dataJson = json.dumps(dataToSend).encode('utf-8')
    #print(dataJson)
    #r = urequests.request('POST',fullAddress,data )
    headers = {'Content-Type': 'application/json'}
    r = urequests.post(fullAddress,data = data,headers = headers)

def getFullAddress(addr: str, api: str) -> str:
    return 'http://{}:1111/{}'.format(addr, api)


def colorDetectedByCamera(img)-> str:
    colorDetected = 'other'
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
            colorDetected = 'green'

    return colorDetected


main()
