# Untitled - By: timothy.woodbridge - Fri May 20 2022

import time

import externalSensors

import processing
import actionEngine
import groundStation




def main() -> None:
    loopPause = 0.25
    externalSensors.initialize()
    groundStation.initialize()
    

    clock = time.clock()

    while(True):
        clock.tick()        

        time.sleep(loopPause)

        externalSensors.collectData()

        processing.parseSensorData()

        #

        #groundStation.sendStatusMessage()

        actionEngine.getNextStep()

        #actionEngine.executeNextStep()               

        
main()
