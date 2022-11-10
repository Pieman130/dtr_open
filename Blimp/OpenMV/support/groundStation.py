import dataClasses 
import logger

class GroundStation:
    def __init__(self,comms,hw):
        self.wifi = comms.wifi
        self.hw = hw

    def addToJsonStatusMsg(self,existingData,varName,data):
        
        if( isinstance(data,str) ):
            dataStr = data
        else:
            dataStr = str(data)  

        if(existingData != ""):
            existingData = existingData + ","

        newData = existingData + '"' + varName + '": "' + dataStr + '"'

        return newData

        
    def sendStatusMessage(self,missionCommander,flightDirector):
        global wifiInfo    
        
        logger.log.verbose('in print status message')
        data = '{"cameraDetectionStr":"' + dataClasses.data.colorDetected + '"'
        ir1_0str = str(int(dataClasses.data.irData))

        data = data + ',"isIrSensorDetection":"' + ir1_0str + '"'

        if (dataClasses.data.lidarDistance == None):
            lidarDistance = 'null'
        else:
            lidarDistance = str(dataClasses.data.lidarDistance)

        data = data + ',"lidarDistance":"' + lidarDistance + '"'

        data = data + ',"state_description":"' + missionCommander.currentState.description + '"'
        data = data + ',"state_target":"' + missionCommander.currentState.target + '"'
        data = data + ',"state_action":"' + missionCommander.currentState.action + '"'
        
        data = data + ',"currentManeuver":"' + flightDirector.currentManeuver.description + '"'

        data = data + ',"upMotor":"' + str(flightDirector.currentManeuver.controls.up) + '"'
        data = data + ',"throttleMotor":"' + str(flightDirector.currentManeuver.controls.throttle) + '"'
        data = data + ',"yawMotor":"' + str(flightDirector.currentManeuver.controls.yaw) + '"'
        data = data + ',"servoDoor":"' + str(flightDirector.currentManeuver.controls.servo) + '"'
        data = data + ',"controlAuthority":"' + dataClasses.config.controlAuthority + '"'

        data = self.addToJsonStatusMsg(data,'p_up',dataClasses.gndStationCmd.p_up)
        data = self.addToJsonStatusMsg(data,'i_up',dataClasses.gndStationCmd.i_up)
        data = self.addToJsonStatusMsg(data,'d_up',dataClasses.gndStationCmd.d_up)

        data = self.addToJsonStatusMsg(data,'p_throttle',dataClasses.gndStationCmd.p_throttle)
        data = self.addToJsonStatusMsg(data,'i_throttle',dataClasses.gndStationCmd.i_throttle)
        data = self.addToJsonStatusMsg(data,'d_throttle',dataClasses.gndStationCmd.d_throttle)

        data = self.addToJsonStatusMsg(data,'p_yaw',dataClasses.gndStationCmd.p_yaw)
        data = self.addToJsonStatusMsg(data,'i_yaw',dataClasses.gndStationCmd.i_yaw)
        data = self.addToJsonStatusMsg(data,'d_yaw',dataClasses.gndStationCmd.d_yaw)

        data = self.addToJsonStatusMsg(data,'scalar_up',dataClasses.gndStationCmd.scalar_up)
        data = self.addToJsonStatusMsg(data,'scalar_yaw',dataClasses.gndStationCmd.scalar_yaw)
        data = self.addToJsonStatusMsg(data,'scalar_throttle',dataClasses.gndStationCmd.scalar_throttle)


        data = self.addToJsonStatusMsg(data,'isMicroPython',dataClasses.config.isMicroPython)

           
        data = self.addToJsonStatusMsg(data,'error_rounding_up',dataClasses.gndStationCmd.error_rounding_up)
        data = self.addToJsonStatusMsg(data,'error_scaling_up',dataClasses.gndStationCmd.error_scaling_up)
        data = self.addToJsonStatusMsg(data,'pid_min_up',dataClasses.gndStationCmd.pid_min_up)

        data = self.addToJsonStatusMsg(data,'pid_min_up',dataClasses.gndStationCmd.pid_min_up)


        data = self.addToJsonStatusMsg(data,'loopTime',dataClasses.rawData.lastLoopTime)        


        data = self.addToJsonStatusMsg(data,'orangeGoalIsFound',dataClasses.data.orangeGoalIsFound)   
        data = self.addToJsonStatusMsg(data,'yellowGoalIsFound',dataClasses.data.yellowGoalIsFound)   
        data = self.addToJsonStatusMsg(data,'ballIsFound',dataClasses.data.ballIsFound)   
        

        data = self.addToJsonStatusMsg(data,'imu_yaw',dataClasses.rawData.imu_yaw)
        data = self.addToJsonStatusMsg(data,'imu_yaw_rate',dataClasses.rawData.imu_yaw_rate)

        data = self.addToJsonStatusMsg(data,'imu_yaw_limited',dataClasses.data.imu_yaw_limited)
        data = self.addToJsonStatusMsg(data,'imu_yaw_rate_limited',dataClasses.data.imu_yaw_rate_limited)
        
        
        data = self.addToJsonStatusMsg(data,'dist_yellow_goal', dataClasses.data.dist_yellow_goal)
        data = self.addToJsonStatusMsg(data,'dist_orange_goal', dataClasses.data.dist_orange_goal)
                


        logs = logger.log.getLogsForServerAndClear()
        
        logsEscaped = logs.replace('\n',"\\n")
        logsEscaped = logsEscaped.replace('\t',"\\t")

        data = data + ',"logs":"' + logsEscaped + '"'        
        

        data = data +  '}'

        #logger.log.verbose(data)
        #r = urequests.request('POST',fullAddress,data )
        headers = {'Content-Type': 'application/json'}

        fullAddress = self.wifi.getFullAddress(self.wifi.ip,'debug/status')        

        logger.log.verbose("about to post data to: " + fullAddress)

        #a = uping.ping(wifiInfo.ip) # - EINVAL error.. ? why
        
        try:
            r = self.wifi.post(fullAddress,data = data,headers = headers)            
                    
            logger.log.verbose('status to server success! received response.')                          
            self.storeGndStationCmds(r)

        except Exception as e:
            self.hw.turnOnNotConnectedToGndStationLight()
            
            logger.log.warning('cannot connect to server')
            #logger.log.warning(e.msg)
            
    def storeGndStationCmds(self,cmds):
        jsonList = cmds.json()
        jsonDict = jsonList[0]                    
                

        self.hw.turnOnConnectedToGndStationLight()
        dataClasses.gndStationCmd.requestedState = jsonDict['requestedState']
        dataClasses.gndStationCmd.firstManeuver = jsonDict['firstManeuver']
        dataClasses.gndStationCmd.secondManeuver = jsonDict['secondManeuver']
        dataClasses.gndStationCmd.baseUpVal = jsonDict['baseUpVal']
        dataClasses.gndStationCmd.duration = jsonDict['duration']

        dataClasses.gndStationCmd.p_up = jsonDict['p_up']
        dataClasses.gndStationCmd.i_up = jsonDict['i_up']
        dataClasses.gndStationCmd.d_up = jsonDict['d_up']

        dataClasses.gndStationCmd.p_throttle = jsonDict['p_throttle']
        dataClasses.gndStationCmd.i_throttle = jsonDict['i_throttle']
        dataClasses.gndStationCmd.d_throttle = jsonDict['d_throttle']
        
        dataClasses.gndStationCmd.p_yaw = jsonDict['p_yaw']
        dataClasses.gndStationCmd.i_yaw = jsonDict['i_yaw']
        dataClasses.gndStationCmd.d_yaw = jsonDict['d_yaw']            
        dataClasses.gndStationCmd.requestedState = jsonDict['requestedState'] 

        dataClasses.gndStationCmd.manual_up = jsonDict['manual_up'] 
        dataClasses.gndStationCmd.manual_throttle = jsonDict['manual_throttle'] 
        dataClasses.gndStationCmd.manual_yaw = jsonDict['manual_yaw'] 
        dataClasses.gndStationCmd.manual_servo = jsonDict['manual_servo'] 

        dataClasses.gndStationCmd.scalar_up = jsonDict['scalar_up'] 
        dataClasses.gndStationCmd.scalar_yaw = jsonDict['scalar_yaw'] 
        dataClasses.gndStationCmd.scalar_throttle = jsonDict['scalar_throttle'] 
        dataClasses.gndStationCmd.controlAuthority = jsonDict['control'] 
        dataClasses.gndStationCmd.assisted_manualHeight = jsonDict['manualHeight']

        dataClasses.gndStationCmd.resetOpenMVforFTPtsfr = jsonDict['resetOpenMVforFTPtsfr']

        dataClasses.gndStationCmd.error_rounding_up = jsonDict['error_rounding_up']
        dataClasses.gndStationCmd.error_scaling_up = jsonDict['error_scaling_up']
        dataClasses.gndStationCmd.pid_min_up = jsonDict['pid_min_up']

        dataClasses.gndStationCmd.doFtpLoadAndReset = jsonDict['doFtpLoadAndReset']
        dataClasses.gndStationCmd.assisted_yawRate = jsonDict['yawRate']
 

