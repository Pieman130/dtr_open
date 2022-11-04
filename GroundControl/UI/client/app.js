// Attaches all modules called by index.html to be running
// to the user app.
// the user app is attached to the application in the index.html file.
console.log("app.js");
var userApp = angular.module('userApp',['appRoutes','jsUtilityServices',
							'mainController','mainModel','mainToServer', 'nvd3module'                          
                        ]) 
.config(function(){
    //console.log('testing user app');
})
