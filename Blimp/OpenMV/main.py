# Untitled - By: timothy.woodbridge - Fri May 20 2022
    # POWERED UP initializing = 'purple'
    # OK, connected to ground station = 'green'
    # OK, Not connected to gnd station = 'lightGreen'         
    # FAIL 'red'

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

    except Exception as e:
        #this is for upython.
        print(e)
        print(".")

import logger

#logger.log.setLevel_info()
logger.log.setLevel_verbose()
#logger.log.setLevel_debugOnly()


import dataClasses

dataClasses.rawData.lidar = 120 #HACK


logger.log.info('is micropython: ' + str(isMicroPython))
dataClasses.config.isMicroPython = isMicroPython

import sensors
import missionCommander
import flightDirector
import groundStation


def main() -> None:
    loopPause = 0

    hw = hardware.Hardware()

    comm = comms.Comms(hw)

    sensorsObj = sensors.Sensors(hw,comm)

    gndStation = groundStation.GroundStation(comm,hw)

    fltDirector = flightDirector.FlightDirector(comm, hw)

    missionCmder = missionCommander.MissionCommander(fltDirector)
    


    while(True):

        start = time.time_ns()
        time.sleep(loopPause)

        logger.log.heartbeat("===============================")
        logger.log.heartbeat("Top of loop")
        logger.log.heartbeat("===============================")

        sensorsObj.collectData()
        
        missionCmder.determineControlAuthority()

        missionCmder.updateState()

        fltDirector.getNextStep()

        fltDirector.executeNextStep()

        gndStation.sendStatusMessage(missionCmder,fltDirector)

        loopTime = time.time_ns() - start

        logger.log.info('Loop time: ' + str(loopTime/1e9))


main()
