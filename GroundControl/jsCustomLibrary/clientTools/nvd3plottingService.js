/* plotting from  http://krispo.github.io/angular-nvd3/#/ */

// a different library - https://syntagmatic.github.io/parallel-coordinates/
angular.module('nvd3module',[])
.factory('D3factory', function(){
    var service = {};    
    service.convertDbDataToChartReadySeriesData = function(dbData,seriesNames,seriesColors,xVar,yVar){         
        /* inputs
            -dbData - result from database in form 0: {col1: data, col2: data, ...}
                                                   1: {col1: data, col2: data, ...}
            -seriesNames
            -seriesColors
            -xVar - column name of db data you want to be plotted using chart for x axis
            -yVar - column name of db data you want to be plotted using chart for y axis

            ** - special input for xVar or yVar:
                    input '*' to use the current key as reference for getting data
                        Ex: keys are: ['numSuccess','numFail','numIncomplete']
                            want to use these keys on the x axis, and the resulting values of each of these keys on y axis
                            input yVar = '*' to achieve this.
        */

        var seriesData =[];
        var keyName = '';                
        var keys = seriesNames;
        
        var useKeyNameForX = false;
        var useKeyNameForY = false;

        if (xVar === '*'){
            useKeyNameForX = true;
        }
        if (yVar === '*'){
            useKeyNameForY = true;
        }        
        
        for (var keyCtr = 0;keyCtr< keys.length; keyCtr++){
            keyName = keys[keyCtr];
            seriesData.push({
                key: keyName,
                values:[],
                color: seriesColors[keyCtr]
            })
            
            if(useKeyNameForX){
                xVar = keyName;
            }
            if(useKeyNameForY){
                yVar = keyName;
            }

            for (var ctr = 0;ctr < dbData.length;ctr++){
                seriesData[keyCtr].values.push({                    
                    x: dbData[ctr][xVar],
                    y: dbData[ctr][yVar]                          
                })
            }
        }        
        return seriesData;
    }
    service.getParallelChartOptions = function(modName){
        // ng if recommended in presentation, otherwise shows up squished if plot starts hidden: https://github.com/krispo/angular-nvd3/issues/259        
        return new Promise(function(resolve,reject){
            if (modName === "mn"){
                var modDimensions=["resultType",
                                "js",
                                "dutyCycle",
                                "startBw",
                                "stopBw",
                                "dwellTimeus",
                                "subbandInterval",
                                "subbandBandwidth",
                                "stepSize",
                                "mnID",
                                "psID" ]
            }else if (modName === "fm"){
                var modDimensions = ["resultType",
                                    "js",
                                    "dutyCycle",
                                    "fmTypeID",
                                    "rate_kHz",
                                    "deviation_kHz",
                                    "fmID",
                                    "psID" ];
            }else if(modName === "all"){
                var modDimensions=["resultType",
                                "js",
                                "dutyCycle",
                                "fmTypeID",
                                "rate_kHz",
                                "deviation_kHz",
                                "startBw",
                                "stopBw",
                                "dwellTimeus",
                                "subbandInterval",
                                "subbandBandwidth",
                                "stepSize",
                                "mnID",
                                "fmID",
                                "psID" ]
            }
            var ret ={
                chart: {
                    type: 'parallelCoordinates',
                    height: 450,
                     width: 1000,
                    margin: {
                        top: 30,
                        right: 10,
                        bottom: 10,
                        left: 10
                    },                                        
                    dimensions: modDimensions                                                                             
                }
            }
            resolve(ret);
        })
        
    }
    service.getParallelChartOptionsDefault = function(){
        return {
            chart: {
                type: 'parallelCoordinates',
                height: 450,
                // width: 600,
                margin: {
                    top: 30,
                    right: 10,
                    bottom: 10,
                    left: 10
                },                
                dimensions: [
                    "economy (mpg)",
                    "cylinders",
                    "displacement (cc)",
                    "power (hp)",
                    "weight (lb)",
                    "0-60 mph (s)",
                    "year"
                ]                
            }
        }
    }
   /* service.getParallelChartDefaultData = function(){
        return new Promise(function(resolve,reject){
            Nvd3ExData.getParallelCoordinatesExData().then(function(result){        
                resolve(result.data);
            })       
        })        
    }*/
    service.getDefaultD3chartOptions = function(graphHeight,xtitle,ytitle){
        return {
            chart: {
                type: 'lineChart',
                height: graphHeight,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 40,
                    left: 55
                },                
                x: function(d){ return d.x; },
                y: function(d){ return d.y; },
                useInteractiveGuideline: true,
                dispatch: {
                    stateChange: function(e){ console.log("stateChange"); },
                    changeState: function(e){ console.log("changeState"); },
                    tooltipShow: function(e){ console.log("tooltipShow"); },
                    tooltipHide: function(e){ console.log("tooltipHide"); }
                },
                xAxis: {
                    axisLabel: xtitle
                },
                yAxis: {
                    axisLabel: ytitle,
                    tickFormat: function(d){
                        return d3.format('.02f')(d);
                    },
                    axisLabelDistance: -10
                },
                callback: function(chart){
                    console.log("!!! lineChart callback !!!");
                }
            }        
        }        
    }
    service.getMultiBarChartOptions = function(){
        return {
            chart:{
                type:'multiBarChart',
                height: 450,
                margin:{
                    top:20,
                    right: 20,
                    bottom: 45,
                    left: 45
                },
                clipEdge: true,
                stacked: true,
                duration: 500,
                xaxis:{
                    axisLabel: 'x',
                    showMaxMin: false,
                    tickFormat: function(d){
                        return d3.format(',f')(d);
                    }
                },
                yaxis:{
                    axisLabel: 'y',
                    showMaxMin: false,
                    tickFormat: function(d){
                        return d3.format(',f')(d);
                    }
                }
            }
        }
    }

    service.getScatterChartOptions = function(pointSize){
        return {
            chart: {                 
                type: 'scatterChart',                
                height: 300,
                color: d3.scale.category10().range(),
                scatter: {
                    onlyCircles: false
                },
                showDistX: true,
                showDistY: true,
                useInteractiveGuideline: true,
                dispatch: {
                    stateChange: function(e){ console.log("stateChange"); },
                    changeState: function(e){ console.log("changeState"); },
                    tooltipShow: function(e){ console.log("tooltipShow"); },
                    tooltipHide: function(e){ console.log("tooltipHide"); }
                },
                tooltip:{   
                    tooltips: true,               
                    contentGenerator: function (e) {                        
                        var series = e.series[0];
                        if (series.value === null) return;                        
                        result = "<h3>J/S: " + e.point.y + "; " + e.series[0].key + "</h3>" //<p></p> <h5>key " + series.key + "</h5>" + "<h5>e.value: " + e.value + "</h5>";                       
                        return result;                                                          
                    } 
                },
                duration: 0,
                pointRange: [pointSize,pointSize],
                xAxis: {
                    axisLabel: 'Duty Cycle %',
                    tickFormat: function(d){
                        return d3.format('.02f')(d);
                    },                    
                },
                yAxis: {
                    axisLabel: 'J/S',
                    tickFormat: function(d){
                        return d3.format('.02f')(d);
                    },
                  //  tickValues: [1,2,3,4,5],
                    axisLabelDistance: -5
                },
                zoom: {
                    //NOTE: All attributes below are optional
                    enabled: false,
                    scaleExtent: [1, 10],
                    useFixedDomain: false,
                    useNiceScale: false,
                    horizontalOff: false,
                    verticalOff: false,
                    unzoomEventType: 'dblclick.zoom'
                }
            }    
        }        
    }
    return service;
})