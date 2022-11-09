const fs = require('fs');
const path = require('path');

var makeProgressBarText = function(currVal,maxVal,units = '', maxTicks=20,tickChar='.'){
    var percent = currVal/maxVal;
    if (percent > 1){
        percent = 1;
    }
    numTicks = Math.floor(percent * maxTicks);
    numBlanks = maxTicks-numTicks;

    var out = '';
    for(var ctr = 0; ctr < maxTicks; ctr ++){
        if(ctr < numTicks){
            out = out + tickChar
        }else{
            out = out + ' ';
        }
        
    }
    var percentPrint = Math.trunc(percent * 100);
    var progBarText = '[' + out + ']  ( ' + currVal + ' of ' + maxVal + ' ' + units + ') - ' + percentPrint + '%';
    return progBarText;

}

var promiseDelay = function(time_ms){
    return new Promise(function(resolve,reject){
        setTimeout(resolve.bind(null,undefined),time_ms);
    })
}

var readToMlFile = function(filepath){    
    const toml = require('./node_modules/toml');   
    try{
        var tomlConfig = toml.parse(fs.readFileSync(filepath));   
    } catch(err){
        var tomlConfig = "";
        console.error("Toml file read error: " + path.resolve(filepath) + "\n" +  err.name + err.message )
        throw new TypeError("Toml file read error.\n\t" + err.name + err.message + "\nfor file: " + path.resolve(filepath))        
    }
    
    return tomlConfig;                     
}

var readToMlFileDebug = function(path){
    //to ml parsing does not require a promise.  to debug file path though using 
    // fs.real path does.
    return new Promise(function(resolve,reject){
        const toml = require('./node_modules/toml');
        fs.realpath(path,function(ret){
            console.log(ret)
            const tomlConfig = toml.parse(fs.readFileSync(path));
            resolve(tomlConfig);
        })
    })		
}

var inputValidator = function(args,typesDesired){
    var errStr = '';
    for (var ctr = 0;ctr<args.length; ctr++){
        if( typeof(args[ctr]) !== typesDesired[ctr] ) {
            errStr = errStr + "arg[" + ctr + "]: " + args[ctr] + " - NOT TYPE '" + typesDesired[ctr] + "'\n"
        }
    }
    
    if (errStr !== ''){
        let callingFcn = getCallingFunctionPath()
        errStrToPrint = "\nINPUT VALIDATOR:\n\t Error from: " + callingFcn + "\n" +  errStr;
        throw new Error(errStrToPrint);
    }
}

var getCallingFunctionPath = function(){
    let ret = new Error().stack.split("at ")[3].trim();
    return ret;
}

var getCallingFunctionName = function(){
	let tmp = new Error().stack.split("at ")[3].trim();
    let idx = tmp.lastIndexOf("\\")+1
    let ret = tmp.substring(idx,tmp.length-1)
    return ret;
}

var convertStringArrayToCsvList = function(arr){
    var ret="";
    for (var ctr = 0 ; ctr < arr.length; ctr++){
        if (ctr !==0)
        {
            ret = ret + ",";
        }
        ret = ret + arr[ctr];
    }
    return ret;
}
function evalBetter(obj){
    return Function('"use strict";return(' + obj + ')')();
}  

var ander = function(str1,str2){
    if (isSomething(str1) && isSomething(str2)){
        return str1 + " and " + str2;
    }else if( ( isSomething(str1) === 0 ) && ( isSomething(str2) === 0 ) ){
        return '';
    }else{
        return str1 + str2; //where one of them is nothing, so you will just get the non-nothing returned
    }
}

var isSomething = function(val){
    if ((val === undefined) || (val === null) || (val === '')){
        return 0;
    }
    else{
        return 1;
    }
}
var getInt32fromBytes = function(bytes,sIdx,eIdx,littleEndian=false){    
    var val = new DataView(bytes.buffer.splice(sIdx,eIdx-sIdx));
    return view.getInt32(0,littleEndian)
}

var roundNdigits = function(val,nDigits){
    var divisor = Math.pow(10,nDigits);
    return Math.round((val+Number.EPSILON)*divisor)/divisor;
}

function getBitMask(nBits)
{
    bitMask = Math.pow(2,nBits) - 1; //(1<<nbits) optimized version
    return bitMask;
}

function delayMs(numMs){ //for testing only
    return new Promise(function(resolve,reject){
        setTimeout(function(){
            resolve();
        },numMs);	
    })
}

function removeArrayDuplicates(arr){
    var uniqueArr = arr.filter(onlyUnique);
    function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
      }
    return uniqueArr;
}

function convertJsDateToUtc(jsDate){
    var utcOffsetHrs = jsDate.getTimezoneOffset()/60;
    jsDate.setHours(jsDate.getHours() + utcOffsetHrs);
    return jsDate;
}

function getTimestamp(inDate){
if(inDate === undefined){
  inDate = new Date();
}
var outDate = inDate.getFullYear() + "_" + //inDate.toLocaleDateString('en-US',{month:'short'}) 
                ('00' + (inDate.getMonth()+1)).slice(-2) + '_' +  
                ('00' + inDate.getDate()).slice(-2) + '_' + 
                ('00' + inDate.getHours()).slice(-2) + '' +  
                ('00' + inDate.getMinutes()).slice(-2) + '' +  
                ('00' + inDate.getSeconds()).slice(-2) 
return outDate;
}


//also in serverFunctions.  need available separately from inside a server.
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

module.exports = {  
    makeDateForSqlServer: makeDateForSqlServer,
    makeProgressBarText: makeProgressBarText,
    promiseDelay: promiseDelay,
    removeArrayDuplicates: removeArrayDuplicates,
    getCallingFunctionName: getCallingFunctionName,
	getCallingFunctionPath: getCallingFunctionPath,
    inputValidator: inputValidator,
	readToMlFile: readToMlFile,
    readToMlFileDebug: readToMlFileDebug,
    getBitMask: getBitMask,  
    getInt32fromBytes: getInt32fromBytes,   
    roundNdigits: roundNdigits,
    convertStringArrayToCsvList: convertStringArrayToCsvList,
    isSomething: isSomething,
    evalBetter: evalBetter,
    ander: ander,
    delayMs: delayMs,
    convertJsDateToUtc: convertJsDateToUtc,
    getTimestamp: getTimestamp
}