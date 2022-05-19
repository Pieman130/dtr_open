const fs = require('fs').promises;

var writeToFile = function(path,data,flags = "a+"){
    return new Promise(function(resolve,reject){        
        fs.writeFile(path,data,{flag: flags}).then(function(){
            resolve();
        })
        .catch(function(){
            reject('write failed');
        })        
    })    
}
module.exports = { 
    writeToFile: writeToFile
}