angular.module('mainModel',[])
.factory('MainModel',function(MainToServer,TimerObjects, $timeout,Objects,UIcomponents){
    var service = {};
    service.getModel = function(){
        return new Promise(function(resolve,reject){
            var obj = {
                status: {},       
                logs: {
                    lines: '',
                    logTime: '',
                },
                numLogLoopsToView: 1,
                intervalTimeMs: 1000,     
                input:{
                    up: null,
                    throttle: null,
                    yaw: null,
                    doorOpen: 0
                },
                getStatus(){
                    MainToServer.getStatus(obj.numLogLoopsToView).then(function(ret){
                        obj.status = ret.data.systemStatus;
                        obj.logs.lines = obj.parseLogLines(ret.data.logger);
                        obj.logs.logTime = ret.data.logger[0].logTime
                    })                    
                },
                parseLogLines(logger){
                    var out = '';
                    for (var ctr = 0; ctr < logger.length; ctr++){
                        out = out + logger[ctr].logLines;                            
                    }
                    return out;
                    
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