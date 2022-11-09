const fs = require('fs');
const fsPr = fs.promises;
var utility = require('./utilityFcns');
var callingFcn = '';
var writeToFile = function(path,data,flags = "a+"){
    return new Promise(function(resolve,reject){        
        fsPr.writeFile(path,data,{flag: flags}).then(function(){
            resolve();
        })
        .catch(function(){
            reject('write failed');
        })        
    })    
}
var fileExists = function(path){
    return fs.existsSync(path);
}
var readFile = function(path){
    return new Promise(function(resolve,reject){
        fsPr.readFile(path).then(function(data){
            resolve(data);
        })
    })
}

var makeDir = function(dir_path){
    
    try{
        fs.mkdirSync(dir_path);
    }
    catch{
        
        throw Error('Failed to make directory: ' + dir_path + '. From: ' + callingFcn);
    }
}

var createDirIfNeeded = function(dir_path){
callingFcn = utility.getCallingFunctionName();
    if(fileExists(dir_path)){
        //do nothing
    }else{
        makeDir(dir_path);
    }
}
var writeObjectToFile = function(path,obj,flags = "a+"){
    return new Promise(function(resolve,reject){   
        var data = JSON.stringify(obj);
        fsPr.writeFile(path,data,{flag: flags}).then(function(){
            resolve();
        })
    })
}
module.exports = { 
    createDirIfNeeded: createDirIfNeeded,
    fileExists: fileExists,
    writeToFile: writeToFile,
    readFile: readFile,
    writeObjectToFile: writeObjectToFile,
    makeDir: makeDir
}