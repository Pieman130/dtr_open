# Untitled - By: timothy.woodbridge - Fri May 20 2022

import time

import externalSensors

import processing
import actionEngine
import groundStation




def main() -> None:

    externalSensors.initialize()
    groundStation.initialize()
    

    clock = time.clock()

    while(True):
        clock.tick()        

        time.sleep(0.5)

        externalSensors.collectData()

        processing.parseSensorData()

        groundStation.sendStatusMessage()

        actionEngine.getNextStep()

        actionEngine.executeNextStep()               

        
main()
