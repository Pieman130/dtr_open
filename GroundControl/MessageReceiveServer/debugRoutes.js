var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();

router.route('/status/')
.post(function(req,res){    
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
                 " , controlAuthority = '" + controlAuthority + "'" 
                 

    sqlTools.sqlRequestPromise(sqlStr)
    .then(function(){
        var valueStr = sqlTools.makeValuesStr(logLines,lastHeartbeat)
        sqlStr = " INSERT INTO loggerPrints(logLines,logTime) " + valueStr
        return sqlTools.sqlRequestPromise(sqlStr);
    })
    .then(function(){
        var valueStr = sqlTools.makeValuesStr(lastHeartbeat,lidarDistance,irSensorDetection,upMotor,throttleMotor,yawMotor,servoDoor,isMicroPython,
            p_up,i_up,d_up,p_throttle,i_throttle,d_throttle,p_yaw,i_yaw,d_yaw,scalar_up,scalar_yaw,scalar_throttle,error_rounding_up, error_scaling_up,pid_min_up)
        sqlStr = " INSERT INTO dataLogs(logTime,lidarDistance,irSensor,upMotor,throttleMotor,yawMotor,servoDoor,isMicroPython," +
                    "p_up,i_up,d_up,p_throttle,i_throttle,d_throttle,p_yaw,i_yaw,d_yaw,scalar_up,scalar_yaw,scalar_throttle," +
                    "error_rounding_up, error_scaling_up,pid_min_up) " + valueStr;
        return sqlTools.sqlRequestPromise(sqlStr);
    })
    .then(function(){
        sqlStr = " SELECT * FROM maneuverToExecute "
        sqlTools.run(sqlStr,res);
    });            
})

module.exports = router;