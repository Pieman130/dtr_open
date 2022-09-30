# Untitled - By: timothy.woodbridge - Fri May 20 2022

import time



try:
    import hardware
    import comms
    import logger
    isMicroPython = True

except Exception as e:
    print(str(e))
    isMicroPython = False
    import sys
    import pathlib

    try:
        baseDir = pathlib.Path(__file__).parent # Get directory of main
        unitDir = (baseDir / "unitTest/").resolve()
        supportDir = (baseDir / "support/").resolve()
        print(unitDir, supportDir)

        sys.path.append(str(unitDir))
        sys.path.append(str(supportDir))

        import hardwareMock
        hardware = hardwareMock

        import commsMock
        comms = commsMock

        import logger

    except Exception as e:
        #this is for upython.
        print(e)
        print(".")

import logger
#logger.log.setLevel_debugOnly()
logger.log.setLevel_info()
#logger.log.setLevel_debugOnly()


import dataClasses


logger.log.info('is micropython: ' + str(isMicroPython))
dataClasses.config.isMicroPython = isMicroPython

import sensors
import processing
import missionCommander
import flightDirector
import groundStation


def main() -> None:
    loopPause = 0.5

    hw = hardware.Hardware()

    comm = comms.Comms(hw)
    
    sensorsObj = sensors.Sensors(hw,comm)        

    gndStation = groundStation.GroundStation(comm,hw)

    fltDirector = flightDirector.FlightDirector(comm,hw)

    missionCmder = missionCommander.MissionCommander(fltDirector)
    


    while(True):

        time.sleep(loopPause)
        logger.log.heartbeat("===============================")
        logger.log.heartbeat("Top of loop")
        logger.log.heartbeat("===============================")
        
        sensorsObj.collectData()

        processing.parseSensorData()
        processing.parseRCSwitchPositions()
        
        if dataClasses.data.sw_door_control is not None:
            logger.log.verbose("DoorSwitch: " + dataClasses.data.sw_door_control)
        if dataClasses.data.sw_flight_mode is not None:
            logger.log.verbose("FlightMode: " + dataClasses.data.sw_flight_mode)
        
        missionCmder.updateState()

        fltDirector.getNextStep()

        fltDirector.executeNextStep()

      #  gndStation.sendStatusMessage(missionCmder,fltDirector)


main()
