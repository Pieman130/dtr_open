# Untitled - By: timothy.woodbridge - Fri May 20 2022    

import time

def run():          
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
    dataClasses.config.isMicroPython = isMicroPython


    import processing


    logger.log.info('is micropython: ' + str(isMicroPython))


    import sensors
    import missionCommander
    import flightDirector
    import groundStation


    loopPause = 0

    hw = hardware.Hardware()

    comm = comms.Comms(hw)

    sensorsObj = sensors.Sensors(hw,comm)

    gndStation = groundStation.GroundStation(comm,hw)

    fltDirector = flightDirector.FlightDirector(comm, hw)

    missionCmder = missionCommander.MissionCommander(fltDirector)
    

    LOOP_TIME_FIXED = 0.2
    
    keepRunning = 1
    while(keepRunning):                    

        start = time.time_ns()
        
        
        logger.log.heartbeat("===============================")
        logger.log.heartbeat("Top of loop")
        logger.log.heartbeat("===============================")
        
        sensorsObj.collectData()
        processing.parseSensorData()
            
        missionCmder.determineControlAuthority()
        

        dataClasses.config.controlAuthority = dataClasses.constants.CONTROL_AUTHORITY_AUTO
        if(dataClasses.config.controlAuthority != dataClasses.constants.CONTROL_AUTHORITY_RC_REMOTE_CONTROL):
            missionCmder.updateState()

            fltDirector.getNextStep()

            fltDirector.executeNextStep()


        fltDirector.executeDoorPosition() # this needs to always run even in manual mode!


        gndStation.sendStatusMessage(missionCmder,fltDirector)
        # logger.log.getLogsForServerAndClear()    #IF COMMENT OUT ABOVE, uncomment this so log buffer will clear!
        

        if(dataClasses.gndStationCmd.doFtpLoadAndReset):
            keepRunning = 0            

        # make loop time fixed
        loopTime = (time.time_ns() - start)/1e9        
        loopPause = LOOP_TIME_FIXED - loopTime
        if(loopPause >0):
            time.sleep(loopPause)
            logger.log.verbose('loop pause added: ' + str(loopPause))        

        loopTime = (time.time_ns() - start)/1e9
        dataClasses.rawData.lastLoopTime = loopTime
        logger.log.info('Loop time: ' + str(loopTime))

        
