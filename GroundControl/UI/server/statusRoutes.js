var links = require('../../jsCustomLibrary/serverTools/requireLinks.js');
var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();

router.route('/heartbeat/')
.post(function(req,res){   
    var numLogLoopsToView = req.body.numLogLoopsToView;
    var numDataPointsToView = 10;

    var output = {
        systemStatus: {},
        logger: {},
        data: {}
    };
    var sqlStr = " SELECT ID, convert(varchar(50),blimpLastHeartbeat,13) as blimpLastHeartbeat, cameraDetectionStr, isIrSensorDetection " +
            ", currentManeuver, state_description,state_target,state_action,lidarDistance, upMotor,throttleMotor,yawMotor,servoDoor " +
            " FROM systemStatus ";
    sqlTools.sqlRequestPromise(sqlStr)
    .then(function(ret){
        output.systemStatus = ret.recordset[0];
        sqlStr = " SELECT TOP " + numLogLoopsToView + " ID,logLines,convert(varchar(50),logTime,13) as logTime FROM loggerPrints ORDER BY ID desc"
        return sqlTools.sqlRequestPromise(sqlStr)
    })
    .then(function(ret){
        output.logger = ret.recordset;
        sqlStr = " SELECT TOP " + numDataPointsToView + " ID,convert(varchar(50),logTime,13) as logTime,lidarDistance,irSensor FROM dataLogs ORDER BY ID desc"
        return sqlTools.sqlRequestPromise(sqlStr)        
    })
    .then(function(ret){
        output.data = ret.recordset;
        res.send(output);
    })

})

router.route('/getLastRequestValues/')
.get(function(req,res){
    var sqlStr = " SELECT * FROM maneuverToExecute " 
    sqlTools.run(sqlStr,res);
})

router.route('/requestsToBlimp/')
.post(function(req,res){

    var manualServo = req.body.manual_servo;
    var manualYaw = req.body.manual_yaw;
    var manualThrottle = req.body.manual_throttle;
    var manualUp = req.body.manual_up;
    
    var p_up = req.body.p_up;
    var i_up = req.body.p_up;
    var d_up = req.body.p_up;
    
    var p_throttle = req.body.p_up;
    var i_throttle = req.body.p_up;
    var d_throttle = req.body.p_up;

    var p_yaw = req.body.p_up;
    var i_yaw = req.body.p_up;
    var d_yaw = req.body.p_up;

    var scalar_up = req.body.scalar_up;
    var scalar_yaw = req.body.scalar_yaw;
    var scalar_throttle = req.body.scalar_throttle;

    var requestedState = req.body.requestedState;

    var sqlStr = " UPDATE maneuverToExecute SET manual_servo = " + manualServo +
                                             ", manual_yaw = " + manualYaw +
                                             ", manual_throttle = " + manualThrottle +
                                             ", manual_up = " + manualUp +
                                             ", p_up = " + p_up +
                                             ", i_up = " + i_up +
                                             ", d_up = " + d_up + 
                                             ", p_throttle = " + p_throttle +
                                             ", i_throttle = " + i_throttle + 
                                             ", d_throttle = " + d_throttle +
                                             ", p_yaw = " + p_yaw +
                                             ", i_yaw = " + i_yaw + 
                                             ", d_yaw = " + d_yaw + 
                                             ", scalar_up = " + scalar_up + 
                                             ", scalar_yaw = " + scalar_yaw +
                                             ", scalar_throttle = " + scalar_throttle +
                                             ", requestedState = " + requestedState
    sqlTools.run(sqlStr,res);
})

module.exports = router;