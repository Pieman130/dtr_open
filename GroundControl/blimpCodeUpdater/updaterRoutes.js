var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var sqlTools = links.sqlTools;
var express = links.express;
var router = express.Router();
var path = require('path')
const fs = require('fs').promises

var supportFolder = path.resolve(__dirname, '../../Blimp/OpenMV/support/');

router.route('/file/:filename')
.get(function(req,res){     
    var filename = req.params.filename;    

    var fullPathToSend = path.resolve(supportFolder +"\\" + filename);
    res.sendFile(fullPathToSend);  
})

router.route('/supportFiles/')
.get(function(req,res){
    var filenames = [];
    fs.readdir(supportFolder).then(function(files){               
        //listing all files using forEach
        files.forEach(function (file) {
            // Do whatever you want to do with the file
            filenames.push(file);
        });
        res.send(filenames);
    })
    .catch(function(err){
        console.log(err);
        res.send('');
    });
})


router.route('/updateStatus/')
.post(function(req,res){
    var updateStatus = req.body.updateStatus;    
    var sqlStr = "UPDATE blimpCodeUploader SET updateStatus = '" + updateStatus + "'";
    sqlTools.run(sqlStr,res);
})

router.route('/markUploadComplete/')
.post(function(req,res){    
    var dt = sqlTools.makeDateForSqlServer();
    var sqlStr = "UPDATE blimpCodeUploader SET lastRunTimeError = '', datetimeLastUpload = '" + dt + "'; UPDATE maneuverToExecute SET doFtpLoadAndReset = 0";    
    sqlTools.run(sqlStr,res);
})

router.route('/openMvRuntimeError/')
.post(function(req,res){
    var runTimeError = req.body.runTimeError;
    runTimeError = sqlTools.handleSingleQuote(runTimeError);    
    var errTime = sqlTools.makeDateForSqlServer()
    var valueStr = sqlTools.makeValuesStr(errTime,runTimeError)
    var sqlStr = "UPDATE blimpCodeUploader SET lastRunTimeError = '" + runTimeError + "'; INSERT INTO errorLogs(errorTime,error)" + valueStr;
    sqlTools.run(sqlStr,res);
})

router.route('/isUploadRequested/')
.get(function(req,res){
    var sqlStr = "SELECT doFtpLoadAndReset FROM maneuverToExecute"
    sqlTools.sqlRequestPromise(sqlStr).then(function(ret){
        res.send({isUploadRequested: ret.recordset[0].doFtpLoadAndReset})
    })    
})

module.exports = router;