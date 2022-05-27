# Untitled - By: timothy.woodbridge - Fri May 20 2022

import sensor, image, time,network,urequests,json,math
import groundStation
import imageProcessing
import uping

SSID='DTR_team_a' # Network SSID
KEY='GoBigRed'  # Network key
GROUND_STATION_IP = '192.168.1.100'

def main() -> None:

    # Init wlan module and connect to network
    wlan = network.WINC()
    wlan.connect(SSID, KEY)

    #q = uping.ping(GROUND_STATION_IP)
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)


    print(wlan.ifconfig())


    clock = time.clock()

    while(True):
        clock.tick()
        img = sensor.snapshot()

        time.sleep(1)
        colorDetected = imageProcessing.colorDetectedByCamera(img)
        #groundStation.sendStatusMessage(GROUND_STATION_IP,colorDetected)
        print(colorDetected)

main()
