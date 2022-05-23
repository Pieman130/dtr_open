var title = "DTR - UI Server ";
console.log(title)
process.title = title;

// get tools
var links = require('../../jsCustomLibrary/serverTools/requireLinks.js');
var express = links.express;
var app = express();
var bodyParser = links.bodyParser; //npm install body-parser --save
var sqlTools = links.sqlTools;

// Setup database
var dbName = "dtr";
var os = require('os');
var serverName = os.hostname();
sqlTools.createDbConnection(serverName,dbName);


//setup server message handling
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({extended: true}));

//setup routes
var statusRoute = require('./statusRoutes.js');
app.use('/status/',statusRoute);

var port = process.env.PORT || 4000;
app.listen(port,function(){
    console.log('Running server on port ' + port);
})

//UI SETUP - add support files
var projectPath = "C:/DroneRepos/DTRRepo/GroundControl/UI"
var frontEndPath = projectPath + "/client";
var jsCustomLibraryPath = "C:/DroneRepos/DTRRepo/GroundControl/jsCustomLibrary"
var serverToolsPath  = jsCustomLibraryPath + "/serverTools";
var clientToolsPath  = jsCustomLibraryPath + "/clientTools";
app.use(express.static(frontEndPath));
app.use(express.static(serverToolsPath));
app.use(express.static(clientToolsPath));


app.set('view engine', 'ejs');


process.on('unhandledRejection',(reason,p)=>{
    console.log('unhandled rejection at promise',p,'reason:',reason);
})