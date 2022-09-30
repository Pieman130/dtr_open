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
    var lidarDistance_ft = req.body.lidarDistance;

    var sqlStr = " UPDATE systemStatus SET blimpLastHeartbeat = '" + lastHeartbeat + 
                "', cameraDetectionStr = '" + cameraDetectionStr + "'" +
                 " ,isIrSensorDetection = " + irSensorDetection  +
                 " ,currentManeuver = '" +  currentManeuver + "'" +
                 " ,state_description = '" + state_description + "'" +
                 " ,state_target = '" + state_target + "'" +
                 " ,state_action = '" + state_action + "'" +
                 " ,lidarDistance_ft = " + lidarDistance_ft

    sqlTools.sqlRequestPromise(sqlStr)
    .then(function(){
        sqlStr = " SELECT * FROM maneuverToExecute "
        sqlTools.run(sqlStr,res);
    });    
})

module.exports = router;