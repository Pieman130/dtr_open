angular.module('mainModel',[]) 
.factory('MainModel',function(MainToServer,TimerObjects ,D3factory,$timeout,Objects,UIcomponents){
    var service = {};
    service.getModel = function(){
        return new Promise(function(resolve,reject){
            var graphHeight = 20;
            var xtitle = 'x title'
            var ytitle = 'y title'
            var obj = {
                control: '',
                mode: '',                
                status: {},       
                logs: {
                    lines: '',
                    logTime: '',
                },
                numLogLoopsToView: 1,
                intervalTimeMs: 10,                 
                requests:{
                        up: null,
                        throttle: null,
                        yaw: null,
                        doorOpen: 0                                            
                },
                assistedParams: {
                    yawRate: null,
                    heightSetPoint: null
                },
                updateOpenMvCodeStatus:{},
                config: {
                    pid: {
                        up: {
                            p: null,
                            i: null,
                            d: null,
                            error_rounding_up: null,
                            error_scaling_up: null,
                            pid_min_up: null
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
                    requestedState: '',
                    
                },                
                sendRequests(){
                    return new Promise(function(resolve,reject){
                        MainToServer.sendManualControlRequest(obj.requests).then(function(){
                            resolve();
                        })                        
                    })
                },
                sendAssistedParams(){
                    return new Promise(function(resolve,reject){
                        MainToServer.sendAssistedParams(obj.assistedParams).then(function(){
                            resolve();
                        })                        
                    })
                },
                sendControlChange(){
                    return new Promise(function(resolve,reject){
                        let info={
                            control: obj.control,
                            requestedState: ''
                        }
                        if(obj.control === 'manualWeb'){
                            info.requestedState = 'manualTesting'                            
                        }else if(obj.control === 'auto-assisted'){
                            info.requestedState =  obj.mode    
                        }
                        MainToServer.sendControlChange(info).then(function(){
                            resolve();
                        })
                    })
                },
                triggerOpenMVcodeUpload(){
                    return new Promise(function(resolve,reject){
                        MainToServer.triggerOpenMVcodeUpload().then(function(){
                            resolve();
                        })
                    })
                },
                getUploaderStatus(){
                    return new Promise(function(resolve,reject){
                        MainToServer.getUploaderStatus().then(function(ret){
                            var d = ret.data[0];
                            obj.updateOpenMvCodeStatus = d;
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
                                var d = ret.data[0];
                                obj.requests.up = d.up;
                                obj.requests.throttle = d.throttle;
                                obj.requests.yaw = d.yaw;
                                obj.requests.doorOpen = d.doorOpen;

                                obj.config.pid.up.p = d.p_up; 
                                obj.config.pid.up.i = d.i_up;
                                obj.config.pid.up.d = d.d_up;

                                obj.config.pid.throttle.p = d.p_throttle;
                                obj.config.pid.throttle.i = d.i_throttle;
                                obj.config.pid.throttle.d = d.d_throttle;

                                obj.config.pid.yaw.p = d.p_yaw;
                                obj.config.pid.yaw.i = d.i_yaw;
                                obj.config.pid.yaw.d = d.d_yaw;

                                obj.config.scalar.up = d.scalar_up;
                                obj.config.scalar.throttle = d.scalar_throttle;
                                obj.config.scalar.yaw = d.scalar_yaw;

                                obj.config.pid.up.error_rounding_up = d.error_rounding_up;
                                obj.config.pid.up.error_scaling_up = d.error_scaling_up;
                                obj.config.pid.up.pid_min_up = d.pid_min_up;

                                obj.assistedParams.yawRate = d.yawRate
                                obj.assistedParams.heightSetPoint = d.manualHeight 

                                obj.control = d.control;

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
                            })
                            return obj.getUploaderStatus();                            
                        })        
                        .then(function(){
                            resolve();
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