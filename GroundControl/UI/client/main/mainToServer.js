angular.module('mainToServer',[])
.factory('MainToServer',function($http){
    var mainFactory = {};
    mainFactory.getStatus = function(numLogLoopsToView){
        let info = {
            numLogLoopsToView: numLogLoopsToView
        }
        return $http.post('/status/heartbeat/',info);
    }       
    return mainFactory;
})
