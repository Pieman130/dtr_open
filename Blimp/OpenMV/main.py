# Untitled - By: timothy.woodbridge - Fri May 20 2022

import time

import externalSensors

import processing
import actionEngine
import groundStation
#import pixracer


def main() -> None:
    loopPause = 1
    #pixracer.initialize()
    groundStation.initialize() # MUST BE DONE BEFORE EXTERNAL SENSORS.
    externalSensors.initialize() # MUST BE DONE AFTER WIFI INITIALIZATION
    actionEngine.initialize()
    

    clock = time.clock()

    while(True):
        clock.tick()        

        time.sleep(loopPause)

        externalSensors.collectData()

        processing.parseSensorData()
                
        groundStation.sendStatusMessage()

       # actionEngine.updateState()

      #  actionEngine.getNextStep()

       # actionEngine.executeNextStep()               

        
main()
