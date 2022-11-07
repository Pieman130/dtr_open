import imageProcessing
import logger
import time
import dataClasses
import cameraSetup
import sensor


LOOP_TIME_FIXED = 0.2


camera = cameraSetup.OpenMVcamera(sensor)

while(True):


    dataClasses.rawData.img = camera.snapshot()     
    start = time.time_ns()

    imageProcessing.find_ball(dataClasses.rawData.img)
    imageProcessing.find_yellow_goal(dataClasses.rawData.img)
    imageProcessing.find_orange_goal(dataClasses.rawData.img)


    logger.log.verbose('yellow x error' + str(dataClasses.data.goal_yellow_xerror) )
    logger.log.verbose('yellow y error' + str(dataClasses.data.goal_yellow_goal_yerror) )

    logger.log.verbose('orange x error' + str(dataClasses.data.goal_orange_xerror) )
    logger.log.verbose('orange x error' + str(dataClasses.data.goal_orange_goal_yerror) )

    logger.log.verbose('ball x error: ' + str(dataClasses.data.ball_xerror) )
    logger.log.verbose('ball y error: '  + str(dataClasses.data.ball_yerror) ) 

    logger.log.verbose('ballIsFound: ' + str(dataClasses.data.ballIsFound) )
        

    logger.log.verbose("color detected: " + dataClasses.data.colorDetected)

    loopTime = (time.time_ns() - start)/1e9
    loopPause = LOOP_TIME_FIXED - loopTime
    if(loopPause >0):
        time.sleep(loopPause)
        logger.log.verbose('loop pause added: ' + str(loopPause))
    
    logger.log.getLogsForServerAndClear()    
