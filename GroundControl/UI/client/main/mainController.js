console.log("mainController.js");
angular.module('mainController', [])
.controller('mainCtrl',function($scope,MainModel){ 
    
    init();

    function init(){    
        return new Promise(function(resolve,reject){
            MainModel.getModel()
            .then(function(model){                 
                $scope.m = model;  
                model.getStatus();
                resolve();
            })
        })        
    }
})
