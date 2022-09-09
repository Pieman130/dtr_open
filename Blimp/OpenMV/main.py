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

    try:
        sys.path.append('C:\\DroneRepos\\DTRRepo\\Blimp\\OpenMV\\unitTest')
        sys.path.append('C:\\DroneRepos\\DTRRepo\\Blimp\\OpenMV\\support')

        import hardwareMock
        hardware = hardwareMock

        import commsMock
        comms = commsMock
    except:
        #this is for upython.
        print(".")


import dataClasses
print('is micropython: ' + str(isMicroPython))
dataClasses.config.isMicroPython = isMicroPython


import sensors
import processing
import actionEngine
import groundStation


def main() -> None:
    loopPause = 1

    hw = hardware.Hardware()

    comm = comms.Comms(hw)

    sensors.swInitialization(hw,comm)

    gndStation = groundStation.GroundStation(comm,hw)


    action = actionEngine.ActionEngine(comm)


    while(True):

        time.sleep(loopPause)

        sensors.collectData()

        processing.parseSensorData()

        gndStation.sendStatusMessage()

        action.updateState()

        action.getNextStep()

        action.executeNextStep()


main()
