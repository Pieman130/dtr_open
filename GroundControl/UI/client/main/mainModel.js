angular.module('mainModel',[]) 
.factory('MainModel',function(MainToServer,TimerObjects ,D3factory,$timeout,Objects,UIcomponents){
    var service = {};
    service.getModel = function(){
        return new Promise(function(resolve,reject){
            var graphHeight = 20;
            var xtitle = 'x title'
            var ytitle = 'y title'
            var obj = {
                status: {},       
                logs: {
                    lines: '',
                    logTime: '',
                },
                numLogLoopsToView: 1,
                intervalTimeMs: 1000, 
                requests:{
                        up: null,
                        throttle: null,
                        yaw: null,
                        doorOpen: 0                                            
                },
                config: {
                    pid: {
                        up: {
                            p: null,
                            i: null,
                            d: null
                        },
                        throttle: {
                            p: null,
                            i: null,
                            d: null
                        },
                        yaw: {
                            p: null,
                            i: null,
                            d: null
                        }
                    },
                    scalar: {
                        up: null,
                        throttle: null,
                        yaw: null
                    },
                    requestedState: ''
                },                
                sendRequests(){
                    return new Promise(function(resolve,reject){
                        MainToServer.sendManualControlRequest(obj.requests).then(function(){
                            resolve();
                        })                        
                    })
                },
                sendConfig(){
                    return new Promise(function(resolve,reject){
                        MainToServer.sendConfigValues(obj.config).then(function(){
                            resolve();
                        })                        
                    })
                },
                getLastControlRequestedValues(){
                    return new Promise(function(resolve,reject){
                        MainToServer.getLastControlRequestedValues().then(function(ret){
                            $timeout(function(){
                                obj.requests = ret.data[0];
                                resolve();
                            })                            
                        })
                    })                    
                },
                plotting:{
                    options: D3factory.getDefaultD3chartOptions(graphHeight,xtitle,ytitle),
                    data: {}
                },
                getStatus(){
                    return new Promise(function(resolve,reject){
                        MainToServer.getStatus(obj.numLogLoopsToView).then(function(ret){
                            obj.status = ret.data.systemStatus;
                            obj.logs.lines = obj.parseLogLines(ret.data.logger);
                            obj.logs.logTime = ret.data.logger[0].logTime;
                            var dbData = ret.data.data;
                            var seriesNames = ["test"];
                            var seriesColors = ["green"];
                            var xVar = "ID";
                            var yVar = "irSensor";
                            var plotData = D3factory.convertDbDataToChartReadySeriesData(dbData,seriesNames,seriesColors,xVar,yVar);
                            $timeout(function(){
                                obj.plotting.data  = plotData;
                                resolve();
                            })
                            
                        })          
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

            obj.getLastControlRequestedValues().then(function(){
                obj.intervalObj = TimerObjects.getRefreshIntervalObj(obj.refreshFcn,obj.intervalTimeMs)
                obj.intervalObj.start();
                resolve(obj);
            })

        })
    }
    return service;

})