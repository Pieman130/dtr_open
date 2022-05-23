console.log('routes.js');

angular.module('appRoutes',['ngRoute'])
.config(function($routeProvider){       
    $routeProvider    
    .when('/',{        
        templateUrl: 'main/main.html', //default route
        controller: 'mainCtrl',
        controllerAs: 'mainCtrl'
    })
    .when('/main',{        
        templateUrl: 'main/main.html', //default route
        controller: 'mainCtrl',
        controllerAs: 'mainCtrl'
    })      
})
