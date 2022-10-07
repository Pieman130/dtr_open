var sql = require('./node_modules/mssql');
var util = require('./utilityFcns');

//const debug = require('../../../atat/node_modules/debug')
//const sqllog = debug('sqllog')
//const errlog = debug('errlog')
//const status = debug('status');
//const dev = debug('dev')

var pool1 = null;
var poolConnected = null;

var config = {};

function createDbConnection(serverName, dbName){
    config = {
        user: 'mcpc', // verified
        password: 'mcpc', // verified
        server: serverName,//'MCPC100-PC', //serverName, //when running from debugger... how to manage this?
        database: dbName
    };

    config.server = serverName;
    console.log("server: " + config.server + ", db: " + config.database);  
    pool1 = new sql.ConnectionPool(config);
    poolConnected = pool1.connect();
    pool1.on('error',err=>{
        console.log(err);    
    })
}


var run = function(sqlStr,res){
    sqlRequestPromise(sqlStr)
    .then(function(ret){
      results = readDbPromiseForNgRepeat(ret);
      if(results === undefined){
        results = null; // could happen as a result of an update statement.
      }
      res.send(JSON.stringify(results));
    })
    .catch(err=>{
      res.send(null);
      console.log(err);     
    })
}
var makeDateForSqlServer = function(inDate){
    if (inDate === undefined){
        var inDate = new Date;
    }
    var outDate = inDate.getFullYear() + '-' +
        ('00' + (inDate.getMonth()+1)).slice(-2) + '-' +
        ('00' + inDate.getDate()).slice(-2) + ' ' + 
        ('00' + inDate.getHours()).slice(-2) + ':' + 
        ('00' + inDate.getMinutes()).slice(-2) + ':' + 
        ('00' + inDate.getSeconds()).slice(-2) + '.' +
        ('00' + inDate.getMilliseconds()).slice(-3);    
    return outDate;
}
var makeDateTime2ForSqlServer = function(inDate,ns){
    var dateTime = makeDateForSqlServer(inDate);    
    var dateTime2noFractional = dateTime.slice(0,dateTime.length-3) 
    var nsStr = ns.toString();
    nsStr = nsStr.padStart(9,'0');
    var dateTime2 = dateTime2noFractional + nsStr;  
    return dateTime2;
}

var smartInsert = function(idField,cmd){  
    return new Promise(function(resolve,reject){
        var parsedCmd = parseInsertIntoCmd(cmd);
        var isValid = isValidInsertCmd(parsedCmd);
        if (isValid){
            isInsertAlreadyInDb(parsedCmd).then(function(result){
                //console.log("idField: " + idField);
                //console.log("cmd: " + cmd);
                if (result.recordset.length > 0)
                {
                    var record = result.recordset[0];                    
                    resolve(record[idField]);
                }else{
                    cmd = cmd + "; SELECT SCOPE_IDENTITY() as id";
                    sqlRequestPromise(cmd).then(function(ret){
                        resolve(ret.recordset[0].id); // returns a promise
                    })
                    
                }
            })            
        }else{
            reject(new Error("InvalidInput:Invalid Insert command, # fields don't match # values: " + cmd));
        }
    })         

    function isInsertAlreadyInDb(parsedCmd){        
        var sqlStr = "SELECT TOP 1 * FROM " + parsedCmd.tableName + " WHERE ";
        for (var ctr=0;ctr < parsedCmd.fields.length; ctr++){
            if (ctr > 0)
            {
                sqlStr = sqlStr + " AND ";
            }
            sqlStr = sqlStr + parsedCmd.fields[ctr] + " = " + parsedCmd.values[ctr];
        }
        return sqlRequestPromise(sqlStr)        
    }                      
}
var isValidInsertCmd=function(parsedCmd){
    if (parsedCmd.fields.length === parsedCmd.values.length)
    {        
        return true;
    }else{
        return false;
    }
}

var parseInsertIntoCmd=function(cmd)
{  
    var r={};    
    //var tmpIdx = cmd.indexOf(" ");
    cmd = cmd.replace(/\s\s+/g,' '); // replace double space with a single space   

    var tmp = cmd.split(" ");
    var tblEndIdx = tmp[2].indexOf("(");
    r.tableName = tmp[2].substring(0,tblEndIdx);
    var fieldsEndIdx = cmd.indexOf(")");

    var fieldsStartIdx = cmd.indexOf("(")+1;
    var fieldsEndIdx = cmd.indexOf(")");
    var fieldsChar = cmd.substring(fieldsStartIdx,fieldsEndIdx);    
    r.fields = fieldsChar.split(",");

    var valuesTxt = "VALUES(";
    var valuesStartIdx = cmd.indexOf(valuesTxt) + valuesTxt.length;
    var valuesStopIdx = cmd.lastIndexOf(")");
    var valuesChar = cmd.substring(valuesStartIdx,valuesStopIdx)
    r.values = valuesChar.split(",");

    return r;
}
var insertBlobToDb = function(data,fieldName,tableName){
    return new Promise(function(resolve,reject){        
        var sqlStr = 'INSERT INTO ' + tableName + '(' + fieldName + ') VALUES(@' + fieldName + '); SELECT SCOPE_IDENTITY() as id';
        insertBlobToDbWorker(data,fieldName,sqlStr).then(function(ret){
            resolve(ret);
        });                
    })
}
var updateDbWithBlob = function(data,fieldName,tableName,idFieldName,idVal){
    return new Promise(function(resolve,reject){     
        var sqlStr = 'UPDATE ' + tableName + ' SET ' + fieldName + ' = @' + fieldName + ' WHERE ' + idFieldName + ' = ' + idVal;
        insertBlobToDbWorker(data,fieldName,sqlStr).then(function(){
            resolve();
        });                
    });
}
var insertBlobToDbWorker = function(data,fieldName,sqlStr){
    return new Promise(function(resolve,reject){
        var binBuff = new Buffer(data,'binary');
        var ps = new sql.PreparedStatement(pool1);
        ps.input(fieldName,sql.VarBinary);
        ps.output('id',sql.Int);          
        ps.prepare(sqlStr,function(err){
            ps.execute({[fieldName]: binBuff},function(err,records){
                if (records.recordset === undefined){
                    var insertID = null;
                }else{
                    var insertedId = records.recordset[0].id;
                }                
                ps.unprepare(function(err){
                    if (err !== null)
                    {
                        console.log(err);
                        reject();
                    }            
                    /*else{
                        resolve();
                    } */                           
                })
                resolve(insertedId);                
            })
        })
    })
}

var makeValuesStr = function(){
    //expects in inputs
    var result = " VALUES(";
    
    for (var ctr = 0; ctr < arguments.length; ctr++){
        if (ctr !== 0){
            result = result + ",";
        }        
        if (isNaN(arguments[ctr]))
        {
            var valStr = "'" + handleSingleQuote(arguments[ctr]) + "'";            
        }else if((arguments[ctr] === undefined) || (arguments[ctr] === '')){
            var valStr = null;
        }else{
            var valStr = arguments[ctr];
        }

        result = result + valStr;
    }
    result = result + ") ";    
    return result;
}
var buildWhereStr = function(whereStr,fieldName,compareStr,val,isSingleQuote = 0){
    /* val = null currently treated as valid.  have to input 'IS' or 'IS NOT' in compareStr

       return '' if
        - val = ''
        - val = undefined
    */

    /* example: 
        whereStr = sqlTools.buildWhereStrAddSingleQuotes(whereStr,'errTime','>=',startDate);
        whereStr = sqlTools.buildWhereStrAddSingleQuotes(whereStr,'errTime','<=',stopDate);
        whereStr = sqlTools.buildWhereStr(whereStr,'atatTestID','=',atatTestID);
        whereStr = sqlTools.buildWhereStr(whereStr,'deviceID','=',deviceID);
        whereStr = sqlTools.buildWhereStr(whereStr,'errorTypeID','=',errorTypeID);
    */

    return buildWhereStrWorker(whereStr,fieldName,compareStr,val,isSingleQuote);
}
var buildWhereStrAddSingleQuotes = function(whereStr,fieldName,compareStr,val){
    return buildWhereStrWorker(whereStr,fieldName,compareStr,val,1);
}

var buildWhereStrWorker = function(whereStr,fieldName,compareStr,val,isSingleQuote){
    var andStr ='';

    var whereSubStr = buildWhereSubStr(fieldName,compareStr,val,isSingleQuote);        
    if (whereSubStr === ''){
        //do nothing, return whereStr as is.
    }else{
        if(whereStr !== '')
        {
            andStr = ' AND ';
        }else{
            whereStr = ' WHERE ';
        }
    
        whereStr = whereStr + andStr + whereSubStr;      
    }    
    
    return whereStr;
}
var buildWhereSubStr = function(fieldName,compareStr,val,isSingleQuote = 0){
    var andStr ='';
    if (val === '' || val === undefined){
        whereSubStr = '';
    }else{
        if(compareStr.toUpperCase() === "LIKE"){
            val = "'%" + val + "%'";                        
        }else if (isSingleQuote){ // straight string compare
            val = "'" + val + "'";            
        }                
        whereSubStr = fieldName + ' ' + compareStr + ' ' + val;        
    }
    return whereSubStr;
}
var buildWhereAddORfromSubstrFcns = function(whereStr,substrFcns){
    var andStr ='';
    var orFullStr = '';
    var orStr = '';      

    for (var ctr = 0; ctr < substrFcns.length; ctr++){
        orStr = substrFcns[ctr](); 
        if (orFullStr === ''){
            orFullStr = orStr;
        }else if(orFullStr !== '' && orStr != ''){
            orFullStr = orFullStr + " OR " + orStr;        
        }
    }
    if (orFullStr !== ""){
        if (whereStr !== ''){
            andStr = ' AND ';
        }else{
            whereStr = ' WHERE ';
        }  
        whereStr = whereStr + andStr + " ( " + orFullStr + " ) ";
    }
    
    return whereStr;

}

var makeOrStr = function(fieldName,orConditionArray){
    var orStr = "";
    orConditionArray.forEach(x=>{
        if(orStr !== ""){                    
            orStr = orStr + " OR ";
        }
        orStr = orStr + fieldName + " = " + x
    })
    return orStr;
}
var sqlRequestPromise = function(sqlStr,allowSelectScopeIdentity){   
    
    //console.log("before: " + sqlStr);
    if(sqlStr.substr(0,1) === " "){
        sqlStr = sqlStr.substr(1,sqlStr.length);
    }
    //sqlStr = sqlStr.replace(/\s+/, ""); //remove first whitespace.
    //console.log("after: " + sqlStr);
    
    if (allowSelectScopeIdentity === undefined){
        allowSelectScopeIdentity = true;
    } 
    return new Promise(function(resolve,reject){
        //This promise executes a chain of promises and returns an object.
        poolConnected.then( () =>{
            return sqlSelectPromise(pool1,sqlStr,allowSelectScopeIdentity)
        })                
        .then(function(result){
            resolve(result);
        })    
        .catch(function(err){
            err.message = err.message + " SQL: " + sqlStr;      
            //log.error(err);            
            if (err.code === 'ETIMEOUT')             
            {
                //request.cancel();
                console.log('canceled sql request due to ETIMEOUT error');
                //errlog('canceled sql request due to ETIMEOUT error');
            }
            
            reject(err);
        })
    })     
}
var sqlStoredProcedurePromiseBinaryHistogram = function(input){
    return new Promise(function(resolve,reject){

        //mssql stored procedure call for some reason always assumes the datetimes provided are in local time.
        //eliminate this by always subtracting difference between now and utc from any times provided.
        var nowDate = new Date;
        var utcHrOffset = nowDate.getTimezoneOffset()/60;            
        input.startTime = new Date(input.startTime);
        input.stopTime = new Date(input.stopTime);
        input.startTime.setHours(input.startTime.getHours() - utcHrOffset);
        input.stopTime.setHours(input.stopTime.getHours() - utcHrOffset);    

        poolConnected.then( () =>{
            let request = pool1.request();
            request.input('startTime',sql.DATETIME2,input.startTime ); //'2021-4-9 14:44:39.281' //);
            request.input('stopTime',sql.DATETIME2, input.stopTime ); //'2021-4-9 14:44:40.281');x
            request.input('sensorID',sql.Int,input.sensorID);       
            request.output('latestTuneFreqMHz',sql.Float);
            request.output('minTime',sql.DateTime2);
            request.output('maxTime',sql.DateTime2);
            request.execute(input.storedProcedureName)
            .then(function(ret){
                var data = {
                    histogramData: ret.recordsets[0],
                    metaData: {
                        latestTuneFreqMHz:  ret.output.latestTuneFreqMHz,
                        minTime: ret.output.minTime,
                        maxTime:  ret.output.maxTime
                    }
                }                
                resolve(data);
            })
        })
        .catch(function(err){
            console.log("not working");
            console.log(err);
        })            
    })       
}
var sqlStoredProcedureGetSigMfData = function(input){
    return new Promise(function(resolve,reject){            
        poolConnected.then( () =>{
            let request = pool1.request();
            request.input('startTime',sql.DATETIME2,input.startTime ); //'2021-4-9 14:44:39.281' //);
            request.input('stopTime',sql.DATETIME2, input.stopTime ); //'2021-4-9 14:44:40.281');x                
            request.output('firstDetectionTime',sql.DATETIME2);            
            request.execute(input.storedProcedureName)
            .then(function(ret){
                var data = {
                    sigMfData: ret.recordsets[0],
                    metaData: {
                        firstDetectionTime:  ret.output.firstDetectionTime                        
                    }
                }                
                resolve(data);
            })
        })
        .catch(function(err){
            console.log("not working");
            console.log(err);
        })            
    })       
}
var sqlSelectPromise = function(request,qryStr,allowSelectScopeIdentity){
    var isInsert=0;
    return new Promise(function(resolve,reject){
        if ( (qryStr.substring(0,6) === "INSERT") && allowSelectScopeIdentity ){
            isInsert = 1;
            qryStr = qryStr + "; SELECT SCOPE_IDENTITY() as id";
        }
        //sqllog(qryStr);
        request.query(qryStr,function(err,recordset)
        {
            if (err)
            {
                reject(err);
            }
            else{                        
                recordset.isInsert = isInsert;                                    
                resolve(recordset);
            }                                  
        });
    })
}
var readDbPromiseResults=function(results){
    var val = null;
       
    if (results!== null && results !== undefined){
        if (results.recordset.length === 1){   
            if (results.isInsert){
                var val = results.recordset[0].id;
            }
            else{
                var val = results.recordset[0]; // was [0] ... not sure how this will break things...
            }            
        } else if(results.recordset.length > 1){
            var val = results.recordset;
        }
    }   
    return val;     
}
var readDbPromiseForNgRepeat=function(results){
    var val = results.recordset;
    return val;
}
var dateToSqlServerDate = function(jsDate){
    var result = jsDate.getFullYear() + "-" + (jsDate.getMonth()+1) + "-" + jsDate.getDate()
        + " " + jsDate.getHours() + ":" + jsDate.getMinutes() 
        + ":" + jsDate.getSeconds() + "." + jsDate.getMilliseconds();
    //var result = jsDate.toISOString().slice(0,19).replace('T',' '); -- this does UTC time.
    return result;
}
var handleSingleQuote = function(str){
    if (str === undefined){
        return undefined;
    }else{
        return str.replace(/'/g,"''");
    }
    
}

/*********************************************************************************************
 * Chunk insert - take N length array to insert break it up into sql inserts of 1000 rows 
 *          at a time until all data is inserted. 
 * 
 *      Ex:  1050 items to insert in an array.  The result would be two insert statements.
 *          Insert statement 1)
 *                 INSERT INTO tableName(col1,col2,col3) VALUES 
 *                                   (1,2,3), //row 1
 *                                   (2,3,4), //row 2
 *                                    ...
 *                                   (13,16,11) // row 1000
 *          Insert statement 2)
 *                 INSERT INTO tableName(col1,col2,col3) VALUES
 *                              (6,1,4), //row 1001
 *                              (5,1,6), //row 1002
 *                                  ...
 *                              (3,1,6), //row 1005
 * 
 *  NOTE: it is best to use a "chunk" insert into a temporary table so you can compare against
 *           existing table and only insert new values.
 * 
 * Insert Info example: 
 * var insertInfo={
            tableName: "##tmpTestConfig",
            tableColumnNamesArr: ["waveformID","js","psDetailsID","numIterationsPerRun", "myDate"],
            dataColumnNamesArr: ["waveformID","js","psDetailsID","numIterationsPerRun","myDate"],
            charWrappers: ["","","","","'"]   
        }       
**********************************************************************************************/
const defaultDivisor = 1000;
var chunkInsert = function(arrayToBeInserted,insertInfo){
    return new Promise(function(resolve,reject){
        var numElements = arrayToBeInserted.length;
        makeInsertIndexes(numElements,defaultDivisor)
        .then(function(insertIndexes){
            dev('make fm array complete');
            numInsertsNeeded = insertIndexes.length;
            dev("num fm inserts needed to db " + numInsertsNeeded);                                            
    
            if (numInsertsNeeded === 0 ){
                reject(new Error('0 fmArray inserts needed'));
                return;
            }
            var prArr = [];
            for (var ctr = 0;ctr < numInsertsNeeded; ctr++){
                var startIdx = insertIndexes[ctr].startIdx;
                var endIdx = insertIndexes[ctr].endIdx;
                prArr.push(insertArrayChunk(arrayToBeInserted,startIdx,endIdx,insertInfo));                       
            }      
            var results = Promise.all(prArr);
            results.then(()=>{
                resolve(arrayToBeInserted.length);
            })
        });               
    })
}
var makeInsertIndexes = function(numElements,divisor){
    return new Promise(function(resolve,reject){
        //status('makeInsertIndexes')
        if (divisor < 1){
            reject(new Error('makeInsertIndexes divisor < 1'));
            return;
        }
        else{
            var numSlices = Math.ceil(numElements/divisor);
            var result = [];
            var startIdx = 0;            
            var endIdx = 0;
            var numRemaining = numElements;
            for (var ctr = 0;ctr<numSlices;ctr++){
                var remainingRows = numElements - endIdx;
                if (remainingRows > divisor)
                {
                    endIdx = endIdx + divisor;
                }else{
                    endIdx = endIdx + remainingRows               
                }              
                result.push({startIdx: startIdx, endIdx: endIdx})
                startIdx = endIdx;
            }
            resolve(result);
        }
    })
}

var insertArrayChunk = function(insertData,startIdx,endIdx,insertInfo){
    return new Promise(function(resolve,reject){        
        var insertDataSubset = insertData.slice(startIdx,endIdx);  
        if (insertDataSubset.length === 0){
            reject(null);
            return;
        }
    
        make1000InsertRowsSql(insertDataSubset,insertInfo)
        .then(function(sqlStr){
            var allowSelectScopeIdentity = false;
            return sqlRequestPromise(sqlStr,allowSelectScopeIdentity)            
        })
        .then(function(ret){     
            dev('done first insert');              
            resolve(insertDataSubset.length);            
        }) 
        .catch(err=>{      
            console.log(err)
        })              
    })
}

var make1000InsertRowsSql = function(dataArrayToInsert,insertInfo){
    return new Promise(function(resolve,reject){ 
        var numRows;
        if (dataArrayToInsert.length === 0){
            reject(null);
            return;
        }
        else if (dataArrayToInsert.length > 1000)
        {
            numRows = 1000;
        }
        else
        {
            numRows = dataArrayToInsert.length;
        }
        
        resolve(makeChunkInsertSql(numRows,dataArrayToInsert,insertInfo))
    });   
}
var makeChunkInsertSql=function(numRows,dataArrayToInsert,insertInfo){
    return new Promise(function(resolve,reject){
        var sqlStr = "INSERT INTO " + insertInfo.tableName;
        sqlStr = sqlStr + "(" + util.convertStringArrayToCsvList(insertInfo.tableColumnNamesArr) + ")";
        sqlStr = sqlStr + " VALUES ";
        
        var valueRow="";

        for (var ctr=0; ctr< numRows;ctr++)
        {                        
            //sqlStr = sqlStr + "(" + fmArray[ctr].fmTypeID + "," + fmArray[ctr].rateKHz + "," + fmArray[ctr].deviationKHz + ")";
            if (ctr > 0){
                sqlStr = sqlStr + ",";
            }
            valueRow = makeValueRow(dataArrayToInsert,insertInfo.dataColumnNamesArr,insertInfo.charWrappers,ctr);
            sqlStr = sqlStr + "(" + valueRow + ")";            
        } 
       // dev('insert sql for fm:' + sqlStr);
        resolve(sqlStr);
    })      
}
function makeValueRow(data,dataColumnNames,charWrappers,dataIdx){
    var ret="";
    for (var ctr = 0; ctr< dataColumnNames.length; ctr++){
        if (ctr > 0){
            ret = ret + ",";
        }
        ret = ret + charWrappers[ctr] + data[dataIdx][dataColumnNames[ctr]] + charWrappers[ctr];
    }
    return ret;
}

/*************** End chunk insert ********************/

function bulkInsert(dataArray, tableInfo){    
    return new Promise(function(resolve,reject){
        const bulkPool = new sql.ConnectionPool(config);        
    
        bulkPool.connect().then(function(){        
            let req = new sql.Request(bulkPool);
    
            const table = new sql.Table("#detectionsStaging");//tableInfo.tmpTbl);
            table.create = true;
            table.columns.add('id',sql.Int,{nullable:false,primary: true}); //identity: true
            table.columns.add('sensorID',sql.Int), {nullable:false};
            table.columns.add('reportTypeID',sql.Int, {nullable:false});
            table.columns.add('tuneFrequency_MHz',sql.Float, {nullable:false});
            table.columns.add('startFreqBinNum',sql.Int, {nullable:false});
            table.columns.add('freqWidthNumBins',sql.Int, {nullable:false});
            table.columns.add('timeDetected',sql.Char(35), {nullable:false});  
    
            for (let ctr = 0; ctr < dataArray.length; ctr++){
                let d = dataArray[ctr];
                let dt = d.dateTime2ForSqlServer;
                dt = dt.slice(1,dt.length-1); // get rid of start and end quotes.
                table.rows.add(ctr+1,d.sensorID,d.reportType, d.tuneFrequency_MHz, d.startFreqBinNum, d.freqWidthNumBins,dt)            
            }   
    
            req.bulk(table,{tableLock: true}).then(function(){
                //"DBCC TRACEON (610); 
                var sqlStr = "DBCC TRACEON (610);INSERT INTO detections  WITH (TABLOCK) (timeDetected,sensorID,reportTypeID,tuneFrequency_MHz, startFreqBinNum,freqWidthNumBins) " +
                    " SELECT convert(datetime2,timeDetected,21) as timeDetected,sensorID,reportTypeID,tuneFrequency_MHz, startFreqBinNum,freqWidthNumBins " +
                    " from #detectionsStaging ORDER BY timeDetected ASC " +                    
                    "; drop table #detectionsStaging"
                req.query(sqlStr).then(function(ret){ 
                    resolve();                   
                })                
            });               
        })   
    })
              
}

module.exports = { 
    createDbConnection: createDbConnection,
    bulkInsert: bulkInsert,  
    sqlStoredProcedurePromiseBinaryHistogram: sqlStoredProcedurePromiseBinaryHistogram,
    makeDateTime2ForSqlServer:makeDateTime2ForSqlServer, 
    makeDateForSqlServer: makeDateForSqlServer,   
    smartInsert: smartInsert,  
    chunkInsert: chunkInsert,  
    makeInsertIndexes: makeInsertIndexes, // only temporarily needs to be accessed outside.  once chunk insert completed and fully utilized, delete 
    sqlRequestPromise: sqlRequestPromise,
    readDbPromiseForNgRepeat:readDbPromiseForNgRepeat,
    readDbPromiseResults: readDbPromiseResults,
    makeValuesStr: makeValuesStr,   
    dateToSqlServerDate: dateToSqlServerDate,
    handleSingleQuote: handleSingleQuote,
    buildWhereStr: buildWhereStr,    
    buildWhereStrAddSingleQuotes: buildWhereStrAddSingleQuotes,
    buildWhereSubStr: buildWhereSubStr,
    buildWhereAddORfromSubstrFcns: buildWhereAddORfromSubstrFcns,
    insertBlobToDb: insertBlobToDb,
    updateDbWithBlob: updateDbWithBlob,
    run: run,
    makeOrStr: makeOrStr,
    makeChunkInsertSql: makeChunkInsertSql
}


//stack overflow 43663017 bulk insert with node mssql package
/*
var bulkInsert = function(config){
    var connection = new sql.ConnectionPool(config,function(err){
        const table = new sql.table('test');
        table.create =true;
        table.columns.add('id',sql.Int,{nullable:false,primary: true});
        table.columns.add('test',sql.VarChar(max));

        table.rows.add(1,'sup');
        table.rows.add(2,'man');
        table.rows.add(3,'yo');
        const request = new sql.Request();
        return request.bulk(table);        
    });
    
}*/