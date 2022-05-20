var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();

router.route('/status/')
.post(function(req,res){
    var stateID = req.body.stateID;
    var message = req.body.message;
    var lastHeartbeat = sqlTools.makeDateForSqlServer();
    console.log("heartbeat!");
    var sqlStr = " UPDATE systemStatus SET blimpLastHeartbeat = '" + lastHeartbeat + "'";
    sqlTools.run(sqlStr,res);    
})

module.exports = router;