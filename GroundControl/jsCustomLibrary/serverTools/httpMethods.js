const http = require('http');

function isServerReady(options){
    return new Promise(function(resolve,reject){            

        var req = http.request(options,function(res){ 
            res.on('data',function(){                                                
            });     
            res.on('end',function(resp){                        
                resolve(true);
            });
        })
        
        req.on('error',function(e){     
            console.log("is server ready error");               
            resolve(false);
        })                  
        
        req.end();

    })            
                        
}

function postToServer(data,options){
    return new Promise(function(resolve,reject){                                
        options.headers['Content-Length'] = data.length;

        const req = http.request(options,res=>{
            
            res.on('data',d=>{ //forces the server response to be consumed.                                                                 
            })               
                               
            res.on('end',function(resp){ // response is now consumed                        
                resolve();
            });
            
        })                
        req.write(data); //write data to server

        req.on('error',function(e){
            console.log("Can't connect to server! (postToServer)");
            console.log(e)
        })
        
    })
}

function sendAndReceiveFromServer(options){
    return new Promise(function(resolve,reject){
        x = http.request(options,function(res){
            var rawData = [];                
            res.on('data',function(chunk){
                rawData.push(chunk);                
            });                   
            res.on('end',function(){        
              var tmp = Buffer.concat(rawData);
              var x = JSON.parse(tmp);                  
              resolve(x);
            })            
        });
        x.end();

        x.on('error',function(e){
            console.log("Can't connect to server! (sendAndReceiveFromServer)");
            console.log(e)
        })
    })
}

module.exports = {
    isServerReady: isServerReady,
    postToServer: postToServer,
    sendAndReceiveFromServer: sendAndReceiveFromServer
}