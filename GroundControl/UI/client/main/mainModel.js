angular.module('mainModel',[])
.factory('MainModel',function(MainToServer,TimerObjects, $timeout,Objects,UIcomponents){
    var service = {};
    service.getModel = function(){
        return new Promise(function(resolve,reject){
            var obj = {
                status: {},       
                intervalTimeMs: 1000,     
                input:{
                    up: null,
                    throttle: null,
                    yaw: null,
                    doorOpen: 0
                },
                getStatus(){
                    MainToServer.getStatus().then(function(ret){
                        obj.status = ret.data[0];
                    })                    
                },
                refreshFcn(){
                    obj.getStatus()
                }     
            }
            obj.intervalObj = TimerObjects.getRefreshIntervalObj(obj.refreshFcn,obj.intervalTimeMs)
            obj.intervalObj.start();
            resolve(obj);
        })
    }
    return service;

})