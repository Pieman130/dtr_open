const fs = require('fs');
const path = require('path');
var readToMlFile = function(filepath){    
    const toml = require('./node_modules/toml');   
    try{
        var tomlConfig = toml.parse(fs.readFileSync(filepath));   
    } catch(err){
        var tomlConfig = "";
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

function convertJsDateToUtc(jsDate){
    var utcOffsetHrs = jsDate.getTimezoneOffset()/60;
    jsDate.setHours(jsDate.getHours() + utcOffsetHrs);
    return jsDate;
}

function getTimestamp(inDate){
if(inDate === undefined){
  inDate = new Date();
}
var outDate = inDate.getFullYear() +  //inDate.toLocaleDateString('en-US',{month:'short'}) 
                ('00' + inDate.getMonth()).slice(-2) + '' +  
                ('00' + inDate.getDate()).slice(-2) + '_' + 
                ('00' + inDate.getHours()).slice(-2) + '' +  
                ('00' + inDate.getMinutes()).slice(-2) + '' +  
                ('00' + inDate.getSeconds()).slice(-2) 
return outDate;
}

module.exports = {  
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