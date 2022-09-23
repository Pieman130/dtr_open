# Untitled - By: timothy.woodbridge - Fri May 20 2022

import time

try:
    import hardware
    import comms
    isMicroPython = True

except Exception as e:
    print(str(e))
    isMicroPython = False
    import sys
    import pathlib

    try:
        baseDir = str(pathlib.Path(__file__).parent.resolve()) # Get directory of main
        if (sys.platform == "Windows"):
            sys.path.append(baseDir + '\\unitTest')
            sys.path.append(baseDir + '\\support')
        else:   
            sys.path.append(baseDir + "/unitTest")
            sys.path.append(baseDir + "/support")

        import hardwareMock
        hardware = hardwareMock

        import commsMock
        comms = commsMock

    except Exception as e:
        #this is for upython.
        print(e)
        print(".")


import dataClasses
print('is micropython: ' + str(isMicroPython))
dataClasses.config.isMicroPython = isMicroPython


import sensors
import processing
import boss_missionCommander
import boss_flightDirector
import groundStation


def main() -> None:
    loopPause = 1

    hw = hardware.Hardware()

    comm = comms.Comms(hw)

    sensorsObj = sensors.Sensors(hw,comm)    

    gndStation = groundStation.GroundStation(comm,hw)


    missionCommander = boss_missionCommander.MissionCommander()
    flightDirector = boss_flightDirector.FlightDirector(comms)


    while(True):

        time.sleep(loopPause)

        sensorsObj.collectData()

        processing.parseSensorData()
        processing.parseRCSwitchPositions()
        
        missionCommander.updateState()

        flightDirector.getNextStep()

        flightDirector.executeNextStep()

        gndStation.sendStatusMessage(missionCommander,flightDirector)


main()
