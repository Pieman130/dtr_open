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

import ftp
import logger
#logger.log.setLevel_info()
logger.log.setLevel_verbose()
#logger.log.setLevel_debugOnly()


import dataClasses
dataClasses.config.isMicroPython = isMicroPython


import processing

dataClasses.rawData.lidar = 120 #HACK


logger.log.info('is micropython: ' + str(isMicroPython))


import sensors
import missionCommander
import flightDirector
import groundStation

# DEBUGGING ###########################
class DebugControls:
    def __init__(self):
        self.yaw = 0  # -1 to 1
        self.up = 0  # -1 to 1
        self.throttle = 0  # -1 to 1
        self.servo = 0  # 0 for OFF. 1 for ON.
ctrl = DebugControls()
ctrl.up = 0.5
# END DEBUG ###########################


def main() -> None:
    loopPause = 0

    hw = hardware.Hardware()

    comm = comms.Comms(hw)

    sensorsObj = sensors.Sensors(hw,comm)

    gndStation = groundStation.GroundStation(comm,hw)

    fltDirector = flightDirector.FlightDirector(comm, hw)

    missionCmder = missionCommander.MissionCommander(fltDirector)
    

    LOOP_TIME_FIXED = 0.2
    
    while(True):
        
        start = time.time_ns()
        
        
        logger.log.heartbeat("===============================")
        logger.log.heartbeat("Top of loop")
        logger.log.heartbeat("===============================")
        
        sensorsObj.collectData()
        processing.parseSensorData()
            
        missionCmder.determineControlAuthority()

        missionCmder.updateState()

        fltDirector.getNextStep()

        fltDirector.executeNextStep()

        gndStation.sendStatusMessage(missionCmder,fltDirector)
       
        if(dataClasses.gndStationCmd.doFtpLoadAndReset):
            ftpLoadAndReset(hw,comm)

        # make loop time fixed
        loopTime = (time.time_ns() - start)/1e9
        loopPause = LOOP_TIME_FIXED - loopTime
        if(loopPause >0):
            time.sleep(loopPause)
            logger.log.verbose('loop pause added: ' + str(loopPause))        

        loopTime = (time.time_ns() - start)/1e9
        logger.log.info('Loop time: ' + str(loopTime))

       # logger.log.getLogsForServerAndClear()

def ftpLoadAndReset(hw,comm):
    port = 21
    timeout=None
    #logger.log.info("Waiting " + str(timeout) + " sec for new files then reboot.")
    logger.log.getLogsForServerAndClear()
    ftp.ftpserver(port,timeout,comm.wifi.wlan)
    
    hw.led.turnOn('cyan')
    #hw.pyb.hard_reset()

def dumbPid(setVal,lidar):
    if(setVal >= lidar):
        up = 0
    else:
        distanceToGoUp = lidar-setVal
        if distanceToGoUp > 100:
            up = 1
        elif distanceToGoUp > 50:
            up = 0.5
        else:
            up = 0.3
    return up

main()
