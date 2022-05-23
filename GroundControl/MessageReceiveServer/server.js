var title = "DTR - Message Receiver";
console.log(title)
process.title = title;


var dbName = "dtr";

var os = require('os');

var serverName = os.hostname();

var links = require('../jsCustomLibrary/serverTools/requireLinks.js');
var express = links.express;
var app = express();

var bodyParser = links.bodyParser; //npm install body-parser --save

//app must use body parser before it uses the route files!!
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({extended: true}));

var logRoute = require('./debugRoutes.js');
app.use('/debug/',logRoute);

var port = process.env.PORT || 1111;

var sqlTools = links.sqlTools;

sqlTools.createDbConnection(serverName,dbName);

app.set('view engine', 'ejs');


app.listen(port,function(){
    console.log('Running server on port ' + port);
})

process.on('unhandledRejection',(reason,p)=>{
    console.log('unhandled rejection at promise',p,'reason:',reason);
})