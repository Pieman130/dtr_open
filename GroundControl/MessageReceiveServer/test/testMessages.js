const http = require('http');
var os = require('os');

var input = {    
    cameraDetectionStr:    "asdf"
}
var inputJson = JSON.stringify(input);


var options = {
    host: "127.0.0.1",    
    port: 1111,
	path: '/debug/status/',
	method: "POST",
	headers: {
		"Content-Type": "application/json"        
	}
};

console.log("start");

var x = http.request(options,function(res){
    var rawData = [];
    console.log("Connected");
    res.on('data',function(chunk){
        rawData.push(chunk);                
    });
    res.on('end',function(){        
        var tmp = Buffer.concat(rawData);
        var data = JSON.parse(tmp);   
        
        console.log(data);
        console.log("end");
    })
});

x.write(inputJson);
x.end();