angular.module('mainToServer',[])
.factory('MainToServer',function($http){
    var mainFactory = {};
    mainFactory.getStatus = function(numLogLoopsToView){
        let info = {
            numLogLoopsToView: numLogLoopsToView
        }
        return $http.post('/status/heartbeat/',info);
    }   
    mainFactory.getLastControlRequestedValues = function(){
        return $http.get('/status/getLastControlRequestedValues/')
    }    

    mainFactory.sendManualControlRequest = function(info){
        return $http.post('/status/sendControlRequest/',info);
    }
    return mainFactory;
})
