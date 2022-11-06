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
    console.log("requested file: " + filename)

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

router.route('/updateComplete/')
.post(function(req,res){    
    var dt = sqlTools.makeDateForSqlServer();
    var sqlStr = "UPDATE blimpCodeUploader SET datetimeLastUploaded = '" + dt + "'; UPDATE maneuverToExecute SET doFtpLoadAndReset = 0";    
    sqlTools.run(sqlStr,res);
})

router.route('/openMvRuntimeError/')
.post(function(req,res){
    var runTimeError = req.body.runTimeError;    
    var sqlStr = "UPDATE blimpCodeUploader SET runTimeError = '" + runTimeError + "'";
    sqlTools.run(sqlStr,res);
})

router.route('/isUploadReqeuested/')
.get(function(req,res){
    var sqlStr = "SELECT isUploadRequested FROM blimpCodeUploader"
    sqlTools.run(sqlStr,res);
})

module.exports = router;