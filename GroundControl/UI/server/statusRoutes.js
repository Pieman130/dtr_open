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
            ", currentManeuver, state_description,state_target,state_action,lidarDistance, upMotor,throttleMotor,yawMotor,servoDoor,controlAuthority " +
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

router.route('/getLastControlRequestedValues/')
.get(function(req,res){
    var sqlStr = " SELECT manual_up as up, manual_throttle as throttle, manual_yaw as yaw, manual_servo as doorOpen," +
                 " p_up, i_up, d_up, scalar_up," +
                 " p_throttle, i_throttle, d_throttle, scalar_throttle," +
                 " p_yaw, i_yaw, d_yaw, scalar_yaw, " +
                 " control " + 
                 " FROM maneuverToExecute " 
    sqlTools.run(sqlStr,res);
})

router.route('/sendControlChange/')
.post(function(req,res){
    var control = req.body.control;
    var requestedState = req.body.requestedState;
    var sqlStr = "UPDATE maneuverToExecute SET control = '"+ control + "', requestedState = '" + requestedState + "'";
    sqlTools.run(sqlStr,res);
})

router.route('/sendControlRequest/')
.post(function(req,res){
    var up = req.body.up;
    var throttle = req.body.throttle;
    var yaw = req.body.yaw;
    var doorOpen = req.body.doorOpen;
    
    var sqlStr = " UPDATE maneuverToExecute SET manual_servo = " + doorOpen +
                            ", manual_yaw = " + yaw +
                            ", manual_throttle = " + throttle +
                            ", manual_up = " + up
    sqlTools.run(sqlStr,res);
})

router.route('/sendConfigValues/')
.post(function(req,res){
    
    var p_up = req.body.pid.up.p;
    var i_up = req.body.pid.up.i;
    var d_up = req.body.pid.up.d;
    
    var p_throttle = req.body.pid.throttle.p;
    var i_throttle = req.body.pid.throttle.i;
    var d_throttle = req.body.pid.throttle.d;

    var p_yaw = req.body.pid.yaw.p;
    var i_yaw = req.body.pid.yaw.i;
    var d_yaw = req.body.pid.yaw.d;

    var scalar_up = req.body.scalar.up;
    var scalar_yaw = req.body.scalar.yaw;
    var scalar_throttle = req.body.scalar.throttle;

    var requestedState = req.body.requestedState;

    var sqlStr = " UPDATE maneuverToExecute SET p_up = " + p_up +
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
                                             ", requestedState = '" + requestedState + "'"
    sqlTools.run(sqlStr,res);
})

module.exports = router;