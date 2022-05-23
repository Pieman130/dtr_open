angular.module('mainToServer',[])
.factory('MainToServer',function($http){
    var mainFactory = {};
    mainFactory.getStatus = function(){
        return $http.get('/status/heartbeat/');
    }       
    return mainFactory;
})
