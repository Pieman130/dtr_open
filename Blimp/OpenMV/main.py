# Untitled - By: timothy.woodbridge - Fri May 20 2022

import time

import externalSensors

import processing
#import actionEngine
import groundStation
import pixracer
import dataClasses



def main() -> None:
    loopPause = 1
    dataClasses.initialize()
    pixracer.initialize()
    externalSensors.initialize()
    groundStation.initialize()
    # actionEngine.initialize()
    

    clock = time.clock()

    while(True):
        clock.tick()        

        time.sleep(loopPause)

        externalSensors.collectData()

        processing.parseSensorData()
                
        groundStation.sendStatusMessage()

       # actionEngine.updateState()

       # actionEngine.getNextStep()

        #actionEngine.executeNextStep()               

        
main()
