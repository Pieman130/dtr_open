var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();

router.route('/status/')
.post(function(req,res){    
    var cameraDetectionStr = req.body.cameraDetectionStr;
    var lastHeartbeat = sqlTools.makeDateForSqlServer();   
    var irSensorDetection = req.body.isIrSensorDetection;     
    var sqlStr = " UPDATE systemStatus SET blimpLastHeartbeat = '" + lastHeartbeat + "', cameraDetectionStr = '" + cameraDetectionStr + "'" +
                 " ,isIrSensorDetection = " + irSensorDetection ;    
                 sqlTools.sqlRequestPromise(sqlStr)
    .then(function(){
        sqlStr = " SELECT * FROM maneuverToExecute "
        sqlTools.run(sqlStr,res);
    });    
})

module.exports = router;