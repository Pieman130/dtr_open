
angular.module('jsUtilityServices',[])
.factory('MathOps',function(){
    var service = {};
    service.cleanNum = function(value){       
        var result = Math.round(Number(value)*1000000)/1000000;
        return result;        
    }
    return service;
})
.factory('UIcomponents',function(Objects){
    var service = {}
    service.removeAddedAngularTableDataProperties = function(data){
        var tmp = angular.toJson(data); // removes $$hashkey so we can compare (and any other angular added values)
        tmp = JSON.parse(tmp);
        return tmp;
    }
    service.isNewDataAvailableForTable = function(currData,maybeNewData){
        var tmp = service.removeAddedAngularTableDataProperties(currData);
        if(!Objects.deepCompare(tmp,maybeNewData) ){
            return true;
        }else{
            return false;
        }   
    }
    return service;
})
.factory('TimerObjects',function($interval){
    var service = {}
    service.getRefreshIntervalObj = function(myIntervalCode,numMsRefresh){        
        var obj = {  
            interval: {},
            myIntervalCode: myIntervalCode,
            start(){
                obj.interval = $interval(obj.myIntervalCode,numMsRefresh);    
            },
            stop(){
                $interval.cancel(obj.interval);
                obj.interval = undefined;
            }      
        };                 
        return obj;
    }
    service.delay_ms = function(time_ms){
        return new Promise(function(resolve,reject){
            setTimeout(resolve,time_ms);
        })
    }  
    return service;

})
.factory('Utilities',function(Convert){
    //to do, use functions in /app/support/nodeAndAngularTools instead of these.
    var service = {};
    service = {
        isStringAdate: isStringAdate,
        isDateFieldValid: isDateFieldValid, //prob don't need server side
        checkDateRangeStrInputs: checkDateRangeStrInputs, //prob don't need server side
        getColorTriplet: getColorTriplet, //prob don't need server side
        roundToNthDigit: roundToNthDigit,
        dateTime100nsBaseCls: dateTime100nsBaseCls,
        masterTimeCls: masterTimeCls     
    }
    return service;    
    function masterTimeCls(obj, type){
        class MasterTimeCls{
            constructor(obj, type)
            {
                switch (type){
                    case "javascript": //3 digits of fractional second precision
                        this.timeJavascript = obj;
                        break;
                    case "sqlServer":  //3 digits of fractional second precision
                        this.timeSqlServer = obj;
                        break;
                    case "100nsBaseCls": //7 digits of precision, matches sql server date time 2 variable type
                        this.time100nsBase = obj;
                        break;               
                }
            }
            get time100nsBase(){
                return this._time100nsBase.timeStr;
            }
            get time100nsBaseObj(){
                return this._time100nsBase;
            }
            get timeJavascript(){
                var tmp = this._time100nsBase.date;
                tmp.setSeconds(Math.floor(this._time100nsBase.seconds));
                var ms = (this._time100nsBase.seconds - tmp.getSeconds())*1000;
                tmp.setMilliseconds(ms);
                return tmp;
            }
            get timeSqlServer(){
                var tmp = this._time100nsBase.timeStr;
                var lastDecimalIdx = tmp.lastIndexOf('.');
                tmp = tmp.substr(0,lastDecimalIdx + 4);
                return tmp;
            }
            getTimezoneOffsetHrs(){
                var utcOffsetHrs = this.timeJavascript.getTimezoneOffset()/60;
                 return utcOffsetHrs;
            }
            
            set time100nsBase(obj){
                this._time100nsBase = obj;
            }
            set timeJavascript(javascriptDateTime){
                var sqlServerDateTime = Convert.toSqlServerDate(javascriptDateTime);
                this._time100nsBase = service.dateTime100nsBaseCls(sqlServerDateTime);                
            }
            set timeSqlServer(sqlServerDateTime){
                this._time100nsBase = service.dateTime100nsBaseCls(sqlServerDateTime);                
            }                               
            addSeconds(val){
                this._time100nsBase.addSeconds(val);
            }
            addMinutes(val){
                this._time100nsBase.addMinutes(val);
            }
            addHours(val){
                this._time100nsBase.addHours(val);
            }
            addDays(val){
                this._time100nsBase.addDays(val);
            }

            secondsDiff(otherMasterTimeObj){
                var r = this._time100nsBase.secondsDiff(otherMasterTimeObj.time100nsBaseObj);
                return r;
            }

        }
        var masterTimeCls = new MasterTimeCls(obj, type);
        return masterTimeCls;
    }
    function dateTime100nsBaseCls(timeStr){             
        class DateTime100nsBase {
            constructor(timeStr){                        
                this.resetToTimeStr(timeStr);              
            }            
            resetToTimeStr(timeStr){
                var timeStrZeroizedSeconds = this.getDateTimeZeroizedSecond(timeStr);                
                this.date = new Date( timeStrZeroizedSeconds ) 
                this.seconds =  Number( timeStr.substr(timeStr.lastIndexOf(':') +1) );    

                if(isNaN(this.seconds)){
                    console.log("nan!");
                }
            }
            get seconds(){
                return this._seconds;
            }
            set seconds(val){
                this._seconds = service.roundToNthDigit(val,7);
            }                 
            get timeStr(){                
                var tmpTimeStr = Convert.toSqlServerDate(this.date); 
                var r = tmpTimeStr.substr(0,tmpTimeStr.lastIndexOf(':')+1) + this.seconds;               
                return r;
            }       
            getDateTimeZeroizedSecond(dateTimeStr){
                var dateTimeZeroizedSecond = dateTimeStr.substr(0,dateTimeStr.lastIndexOf(':')+1) + "00";
                return dateTimeZeroizedSecond;
            }  
            addSeconds(time_sec){
                if(time_sec >= 0){
                    var secondsSum = this.seconds + time_sec; 
                    var newSeconds = secondsSum % 60;                    
                    var minToAdd = Math.floor(secondsSum/60);

                }else{
                    var minToAdd = Math.ceil(time_sec/60);
                
                    var secondsMinus = time_sec % 60;
    
                    var newSeconds = this.seconds + secondsMinus; 
                    if(newSeconds < 0 ){
                        minToAdd--;
                        newSeconds += 60;
                    }                                 
                }                                

                this.date.setMinutes(this.date.getMinutes() + minToAdd);
                this.seconds = newSeconds;                           
            }   
            addMinutes(minutes){
                this.date.setMinutes(this.date.getMinutes() + minutes);
            }              
            addHours(hours){
                this.date.setHours(this.date.getHours() + hours);
            }
            addDays(days){
                this.date.setDate(this.date.getDate() + days);
            }
            secondsDiff(otherDateTime100nsBase){
                var t1 = new Date(this.date.getTime())
                t1.setSeconds(this.seconds);
                var t2 = new Date(otherDateTime100nsBase.date.getTime());
                t2.setSeconds(otherDateTime100nsBase.seconds);
                var diff_s = (t1.getTime() - t2.getTime())/1000;     
                var minsDiff = Math.floor(diff_s/60);           
                var diff_fract_s = this.seconds - otherDateTime100nsBase.seconds
                if(diff_fract_s < 0){
                    diff_fract_s = diff_fract_s +60;
                }
                var r = minsDiff * 60 + diff_fract_s;
                return r;
            } 
            isGreaterThan(otherDateTime100nsBase){
                if ( this.date.getTime() > otherDateTime100nsBase.date.getTime() ) {
                    return true;
                } else if ( this.date.getTime() === otherDateTime100nsBase.date.getTime() ){
                    if( this.seconds > otherDateTime100nsBase.seconds){
                        return true;
                    }
                } 
                return false;
                
            }
            isGreaterThanOrEqual(otherDateTime100nsBase){
                if ( this.date.getTime() > otherDateTime100nsBase.date.getTime() ) { //! don't put >= here!
                    return true;
                } else if ( this.date.getTime() === otherDateTime100nsBase.date.getTime() ){
                    if( this.seconds >= otherDateTime100nsBase.seconds){
                        return true;
                    }
                } 
                return false;
            }
            isEqual(otherDateTime100nsBase){
                if ( (this.date.getTime() === otherDateTime100nsBase.date.getTime()) && (this.seconds === otherDateTime100nsBase.seconds)){                    
                    return true;                    
                }else{
                    return false;
                }                
            }
            isLessThan(otherDateTime100nsBase){
                if ( this.date.getTime() < otherDateTime100nsBase.date.getTime() ) {
                    return true;
                } else if ( this.date.getTime() === otherDateTime100nsBase.date.getTime() ){
                    if( this.seconds < otherDateTime100nsBase.seconds){
                        return true;
                    }
                } 
                return false;
            }
            isLessThanOrEqual(otherDateTime100nsBase){
                if ( this.date.getTime() < otherDateTime100nsBase.date.getTime() ) { //! don't put <= here!
                    return true;
                } else if ( this.date.getTime() === otherDateTime100nsBase.date.getTime() ){
                    if( this.seconds <= otherDateTime100nsBase.seconds){
                        return true;
                    }
                } 
                return false;
            } 
            /* --tests run.  
            var smaller = Utilities.dateTime100nsBaseCls('2021-2-12 16:32:43.191704');
            var smallerEq = Utilities.dateTime100nsBaseCls('2021-2-12 16:32:43.191704');
            var bigger =  Utilities.dateTime100nsBaseCls('2021-2-12 16:32:43.192');

            console.log("smaller < bigger?: (true)" + smaller.isLessThan(bigger));
            console.log("smaller <= bigger? (true)" + smaller.isLessThanOrEqual(bigger));
            console.log("smaller > bigger?: (false)" + smaller.isGreaterThan(bigger));
            console.log("smaller >= bigger?: (false)" + smaller.isGreaterThanOrEqual(bigger));
            console.log("smaller = bigger?: (false)" + smaller.isEqual(bigger));
            console.log("smaller = smallerEq?: (true)" + smaller.isEqual(smallerEq));
            console.log("bigger >= smaller?: (true)" + bigger.isGreaterThanOrEqual(smaller));              
            */
               
        }   
        var dateTime100nsBase = new DateTime100nsBase(timeStr);        
        return dateTime100nsBase;
    }
    

    function roundToNthDigit(val,numDecimalPlaces){
        var r = Number( Math.round(val + "e" + numDecimalPlaces ) + "e-" + numDecimalPlaces);
        return r;
    }
    function getColorTriplet(color){
        switch (color){                        
            case "red":
                var triplet = "#FF0000"; 
                break;
            case "orange":
                var triplet = "#ffa500";
                break;
            case "yellow":
                var triplet = "#fff200";
                break;
            case "green":
                var triplet = "#00FF00";
                break;  
            case "blue":
                var triplet = "#0541b0"; 
                break;                                  
            case "purple":
                var triplet = "#9F07F7";
                return;
            case "pink":
                var triplet = "#FF00FF"; 
                break;            
            case "white":
                var triplet = "#ffffff";
                break;
            case "black":
                var triplet = "#000000";
                break;
            case "grey":
                var triplet = "#fcfcfc";
                break;
            default:
                var triplet = "#000000";
        }
        return triplet;

    }
    function checkDateRangeStrInputs(startDate,endDate,fcnValidStart,fcnValidEnd,fcnValidRange){        
        var isStartValid = checkDateStr(startDate);
        var isEndValid = checkDateStr(endDate);        
        if (isStartValid && isEndValid){            
            var isValidRange = isValidDateRange(startDate,endDate);
        } else{
            var isValidRange = false;
        }        
        fcnValidStart(isStartValid);
        fcnValidEnd(isEndValid);
        fcnValidRange(isValidRange);
    }

    function isValidDateRange(startDate,stopDate){                     
        if ((startDate === undefined) || (stopDate === undefined)){
            return true; //don't tell them date range is wrong if they aren't done inputting info
        }
        
        return moment(startDate).isBefore(stopDate);
        
    }
    function isStringAdate(dateStr){
        return checkDateStr(dateStr);
    }
    function isDateFieldValid(dateField){
        return checkDateField(dateField);
    }
    function checkDateStr(dateStr){
        var result = false;
        if (dateStr === undefined){
            result = true;
        }
        if (moment(dateStr,"MM/DD/YYYY", true).isValid())
        {
            result = true;
        }
        if (moment(dateStr,"M/DD/YYYY", true).isValid())
        {
            result = true;
        }
        if (moment(dateStr,"MM/D/YYYY", true).isValid())
        {
            result = true;
        }
        if (moment(dateStr,"M/D/YYYY", true).isValid())
        {
            result = true;
        }

        if (moment(dateStr,"MM/DD/YY", true).isValid())
        {
            result = true;
        }
        if (moment(dateStr,"M/DD/YY", true).isValid())
        {
            result = true;
        }
        if (moment(dateStr,"MM/D/YY", true).isValid())
        {
            result = true;
        }
        if (moment(dateStr,"M/D/YY", true).isValid())
        {
            result = true;
        }
        return result;
    } 
    function checkDateField(dateField){
        if (checkDateStr(dateField) || (dateField === undefined))
        {
            return false;
        }else{
            return true;
        }   
    }    
})
.factory('Convert',function(){
    var service = {};
    service.toSqlServerDate = function(jsDate){                
        var result = jsDate.getFullYear() + "-" + (jsDate.getMonth()+1) + "-" + jsDate.getDate()
        + " " + jsDate.getHours() + ":" + jsDate.getMinutes() 
        + ":" + jsDate.getSeconds() + "." + jsDate.getMilliseconds();        
        return result;        
    }    
    return service;
})
.factory('Arrays',function(){    
    var service = {};   
    service.isArray=function(variable){
        return variable.constructor === Array;
    } 
    service.getArrayFromObject = function(obj,propertyName){ 
        return obj.map(function(e){return e[propertyName];});        
    }
    service.getMax = function(arr){
        return Math.max.apply(null,arr)
    }
    service.getMin = function(arr){
        return Math.min.apply(null,arr)
    }
    service.removeFirstElement = function(arr)
    {
        arr.splice(0,1);
        return arr;
    }
    service.removeLastElement = function(arr)
    {
        arr.splice(arr.length-1,1);
        return arr;
    }

    return service;
})
.factory('Classes',function(){
    var service={};
    service.copyByVal = function(cls){
        var newCls = _.cloneDeep(cls);
        return newCls;
    }
    return service;
})
.factory('Objects',function(){
    var service = {};
    service.deepCompare = function(obj1,obj2){
        // Uses lodash library.  match is true as long as there are no conflicting values.  
        if(obj1.length !== obj2.length){
            return false;
        }else{
            var isSameObject = _.isMatch(obj1,obj2);              
            return isSameObject; 
        }
        
    }
    service.getUnequalProperties = function(obj1,obj2){        
        // ONLY goes 1 level deep. since lodash commented out line wasn't working.  failure to reference library.
        const diff = Object.keys(obj1).reduce((result, key) => {
            if (!obj2.hasOwnProperty(key)) {
                result.push(key);
            } else if (_.isEqual(obj1[key], obj2[key])) { // lodash library method.  having trouble with references...
            //} else if (obj1[key] === obj2[key]) {
                const resultKeyIndex = result.indexOf(key);
                result.splice(resultKeyIndex, 1);
            }
            return result;
        }, Object.keys(obj2));
    
        return diff;

    }
    service.addNamedPair = function(obj,propertyName,value){
        obj[obj.length] = {[propertyName]:value};                
        return obj;
    }
    service.getArrayOfObjElementWithThisValue = function(obj,propName,propVal){            
        var val = obj.filter(foundElement => { 
                return foundElement[propName] === propVal
            });                
        return val;
    }
    service.addNamedPairToTop = function(obj,propertyName,value){        
        obj.unshift({[propertyName]:value});
        return obj;
    }
    service.isField = function(obj,fieldName){
        if(obj.hasOwnProperty(fieldName)){
            return true;
        }else{
            return false;
        }
    }
    service.addBlankSubObjects = function(object,propNames){        
        for (var ctr = 0;ctr<propNames.length;ctr++){
            var nextProp = propNames[ctr];            
            object[nextProp] = {};
        }
        return object;
    }
    service.createNestedObject = function(  base,names ) {   
        // from https://stackoverflow.com/questions/5484673/javascript-how-to-dynamically-create-nested-objects-using-object-names-given-by/48751698     
        var createNestedObject = function( base, names ) {            
            for( var i = 0; i < names.length; i++ ) {
                base = base[ names[i] ] = base[ names[i] ] || {};                
            }
        };                        
        createNestedObject( base,names );
        return base;
    }   
    service.createBlankSubproperties = function(object,propNames){
        for(var ctr = 0;ctr<propNames.length;ctr++){                
            var newPropName = propNames[ctr];                
            object[newPropName] = "";
        }  
        return object;
    }
    service.createBlankSubpropertiesToAllProperties = function(object,propNames){        
        for (const property in object){
            for(var ctr = 0;ctr<propNames.length;ctr++){                
                var newPropName = propNames[ctr];                
                object[property][newPropName] = "";
            }            
        }        
        return object;
    }
    service.copyObjCreateNew = function(sourceObj,destObj,newObjNames){
        for (var ctr = 0;ctr<newObjNames.length;ctr++){
            destObj[newObjNames[ctr]] = Object.assign({},sourceObj);
            
            angular.copy(sourceObj,destObj[newObjNames[ctr]]);
        }
    }
    service.copyObj = function(sourceObj,destObj){
        destObj = Object.assign({},sourceObj);        
        return destObj;
    }
    service.copyByVal = function(obj){
        var newCls = _.cloneDeep(obj);
        return newCls;
    }

    return service;
})