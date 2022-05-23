var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();

router.route('/status/')
.post(function(req,res){    
    var cameraDetectionStr = req.body.cameraDetectionStr;
    var lastHeartbeat = sqlTools.makeDateForSqlServer();        
    var sqlStr = " UPDATE systemStatus SET blimpLastHeartbeat = '" + lastHeartbeat + "', cameraDetectionStr = '" + cameraDetectionStr + "'" ;
    sqlTools.run(sqlStr,res);    
})

module.exports = router;