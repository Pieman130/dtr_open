var title = "Blimp Code Updater";
console.log(title)
process.title = title;


var dbName = "dtr";

var os = require('os');
var path = require('path')

var serverName = os.hostname();

var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var express = links.express;
var app = express();

var bodyParser = links.bodyParser; //npm install body-parser --save

//app must use body parser before it uses the route files!!
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({extended: true}));

var updaterRoute = require('./updaterRoutes.js');
app.use('/updater/',updaterRoute);

var supportFolder = path.resolve(__dirname, '../../Blimp/OpenMV/support')
app.use(express.static(supportFolder))

var port = process.env.PORT || 7071;

var sqlTools = links.sqlTools;

sqlTools.createDbConnection(serverName,dbName);

app.set('view engine', 'ejs');


app.listen(port,function(){
    console.log('Running server on port ' + port);
})

process.on('unhandledRejection',(reason,p)=>{
    console.log('unhandled rejection at promise',p,'reason:',reason);
})


/*var express = require('express');
var app = express();

var path = __dirname + '/public';
var port = 8080;

app.use(express.static(path));
app.get('*', function(req, res) {
    res.sendFile(path + '/index.html');
});
app.listen(port);*/