var links = require('../../jsCustomLibrary/serverTools/requireLinks.js');
var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();

router.route('/heartbeat/')
.get(function(req,res){   
    var output = {
        systemStatus: {},
        logger: {}
    };
    var sqlStr = " SELECT ID, convert(varchar(50),blimpLastHeartbeat,13) as blimpLastHeartbeat, cameraDetectionStr, isIrSensorDetection " +
            ", currentManeuver, state_description,state_target,state_action,lidarDistance_ft " +
            " FROM systemStatus ";
    sqlTools.sqlRequestPromise(sqlStr)
    .then(function(ret){
        output.systemStatus = ret.recordset[0];
        sqlStr = " SELECT TOP 1 * FROM loggerPrints ORDER BY ID desc"
        return sqlTools.sqlRequestPromise(sqlStr)
    })
    .then(function(ret){
        output.logger = ret.recordset[0];
        res.send(output);
    })

})

module.exports = router;