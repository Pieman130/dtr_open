angular.module('mainModel',[])
.factory('MainModel',function(MainToServer,TimerObjects, $timeout,Objects,UIcomponents){
    var service = {};
    service.getModel = function(){
        return new Promise(function(resolve,reject){
            var obj = {
                status: {},            
                getStatus(){
                    MainToServer.getStatus().then(function(ret){
                        obj.status = ret.data[0];
                    })                    
                }        
            }
            resolve(obj);
        })
    }
    return service;

})