var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var loggerModule = require('../jsCustomLibrary/serverTools/logger.js');

var isFileLoggingOn = true;
var logger = loggerModule.getLogger(isFileLoggingOn)
logger.filePrefix = "DTR"

var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();

router.route('/status/')
.post(function(req,res){       
    insertStatusToDb()
    .then(function(){
        getManeuverToExecute().then(function(){
            //
        })
    })            
    .catch(function(ex){        
        getManeuverToExecute().then(function(){
            logger.error(ex);            
        })
    })
    
    function getManeuverToExecute(){
        return new Promise(function(resolve,reject){
            sqlStr = " SELECT * FROM maneuverToExecute "
            sqlTools.sqlRequestPromise(sqlStr).then(function(ret){
                res.send(ret.recordset);
                resolve();
            })
        })        
    }    

    function insertStatusToDb(){
        return new Promise(function(resolve,reject){            
            
            var cameraDetectionStr = req.body.cameraDetectionStr;
            var lastHeartbeat = sqlTools.makeDateForSqlServer();   
            var irSensorDetection = req.body.isIrSensorDetection;  
            var currentManeuver = req.body.currentManeuver;   
            var state_description = req.body.state_description;
            var state_target = req.body.state_target;
            var state_action = req.body.state_action;
            var lidarDistance = req.body.lidarDistance;
            var upMotor = req.body.upMotor;
            var throttleMotor = req.body.throttleMotor;
            var yawMotor = req.body.yawMotor;
            var servoDoor = req.body.servoDoor;
            var controlAuthority = req.body.controlAuthority;
            var loopTime = req.body.loopTime;

            var imu_yaw = convertNoneToNull(req.body.imu_yaw);
            var imu_yaw_rate = convertNoneToNull(req.body.imu_yaw_rate);

            var imu_yaw_limited = convertNoneToNull(req.body.imu_yaw_limited);
            var imu_yaw_rate_limited = convertNoneToNull(req.body.imu_yaw_rate_limited);



            var ballIsFound = convertNoneToZero(req.body.ballIsFound);
            var yellowGoalIsFound = convertNoneToZero(req.body.yellowGoalIsFound);
            var orangeGoalIsFound = convertNoneToZero(req.body.orangeGoalIsFound);
        
            yawMotor = convertNanToNull(yawMotor)
            upMotor = convertNanToNull(upMotor)
            throttleMotor = convertNanToNull(throttleMotor)    

            function convertNoneToZero(val){
                if(val === 'None'){
                    val = 0;
                }
                return val;
            }
            function convertNoneToNull(val){
                if (val === 'None'){
                    val = 'null'
                }
                return val;
            }
        
            function convertNanToNull(val){
        
                if(val === 'nan'){
                    ret = 'null'
                    console.log("was nan");
                }else{
                    ret = val
                }
                return ret;
            }
            
            var p_up = req.body.p_up;
            var i_up = req.body.i_up;
            var d_up = req.body.d_up;
        
            var p_throttle = req.body.p_throttle;
            var i_throttle = req.body.i_throttle;
            var d_throttle = req.body.d_throttle;
        
            var p_yaw = req.body.p_yaw;
            var i_yaw = req.body.i_yaw;
            var d_yaw = req.body.d_yaw;
        
        
            var scalar_up = req.body.scalar_up;
            var scalar_yaw = req.body.scalar_yaw;
            var scalar_throttle = req.body.scalar_throttle;
                        
            var error_rounding_up = req.body.error_rounding_up;
            var error_scaling_up = req.body.error_scaling_up;
            var pid_min_up = req.body.pid_min_up;
        
        
            var isMicroPython = req.body.isMicroPython;
        
            if(isMicroPython === 'False'){
                isMicroPython = 0;
            }else{
                isMicroPython = 1;
            }
        
            var logLines = req.body.logs;
        
            var sqlStr = " UPDATE systemStatus SET blimpLastHeartbeat = '" + lastHeartbeat + 
                        "', cameraDetectionStr = '" + cameraDetectionStr + "'" +
                        " ,isIrSensorDetection = " + irSensorDetection  +
                        " ,currentManeuver = '" +  currentManeuver + "'" +
                        " ,state_description = '" + state_description + "'" +
                        " ,state_target = '" + state_target + "'" +
                        " ,state_action = '" + state_action + "'" +
                        " ,lidarDistance = " + lidarDistance +
                        " , upMotor = " + upMotor +
                        " , throttleMotor = " + throttleMotor + 
                        " , yawMotor = " + yawMotor + 
                        " , servoDoor = " + servoDoor + 
                        " , controlAuthority = '" + controlAuthority + "'" +
                        " , ballIsFound = " + ballIsFound +
                        " , yellowGoalIsFound = " + yellowGoalIsFound +
                        " , orangeGoalIsFound = " + orangeGoalIsFound                                                      

            sqlTools.sqlRequestPromise(sqlStr)
            .then(function(){
                var valueStr = sqlTools.makeValuesStr(logLines,lastHeartbeat)
                sqlStr = " INSERT INTO loggerPrints(logLines,logTime) " + valueStr
                return sqlTools.sqlRequestPromise(sqlStr);
            })
            .then(function(){
                var valueStr = sqlTools.makeValuesStr(lastHeartbeat,lidarDistance,irSensorDetection,upMotor,throttleMotor,yawMotor,servoDoor,isMicroPython,
                    p_up,i_up,d_up,p_throttle,i_throttle,d_throttle,p_yaw,i_yaw,d_yaw,scalar_up,scalar_yaw,scalar_throttle,error_rounding_up, error_scaling_up,pid_min_up,controlAuthority,loopTime,
                currentManeuver,state_description,state_target,state_action, ballIsFound,yellowGoalIsFound,orangeGoalIsFound,imu_yaw ,imu_yaw_rate,imu_yaw_limited , imu_yaw_rate_limited)                    

                
                sqlStr = " INSERT INTO dataLogs(logTime,lidarDistance,irSensor,upMotor,throttleMotor,yawMotor,servoDoor,isMicroPython," +
                            "p_up,i_up,d_up,p_throttle,i_throttle,d_throttle,p_yaw,i_yaw,d_yaw,scalar_up,scalar_yaw,scalar_throttle," +
                            "error_rounding_up, error_scaling_up,pid_min_up,controlAuthority,loopTime," +
                            "currentManeuver,state_description,state_target,state_action, ballIsFound,yellowGoalIsFound,orangeGoalIsFound,imu_yaw ,imu_yaw_rate,imu_yaw_limited , imu_yaw_rate_limited) " + valueStr;
                return sqlTools.sqlRequestPromise(sqlStr);
            })
            .then(function(){
                resolve();
            })     
            .catch(function(ex){
                reject(ex.message);
            })                
        })
    }                            

})

module.exports = router;