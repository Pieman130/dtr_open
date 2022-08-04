# Untitled - By: timothy.woodbridge - Fri May 20 2022

import sensor, image, time,network,urequests,json,math
import uping


import externalSensors

import processing
import actionEngine
import groundStation



SSID='DTR_team_a' # Network SSID
KEY='GoBigRed'  # Network key
GROUND_STATION_IP = '192.168.1.100'

def main() -> None:

    # Init wlan module and connect to network
    wlan = network.WINC()
    wlan.connect(SSID, KEY)

    #q = uping.ping(GROUND_STATION_IP)
  


    externalSensors.initialize()

    print(wlan.ifconfig())


    clock = time.clock()

    while(True):
        clock.tick()
        #img = sensor.snapshot()

        time.sleep(0.5)

        externalSensors.collectData()

        processing.parseSensorData()

        actionEngine.getNextStep()
        
       # actionEngine.executeNextStep()               

        #colorDetected = imageProcessing.colorDetectedByCamera(img)
        #groundStation.sendStatusMessage(GROUND_STATION_IP,colorDetected)
        #print(colorDetected)

main()
