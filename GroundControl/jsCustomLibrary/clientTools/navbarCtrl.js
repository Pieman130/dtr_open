angular.module('mainNavBarController',['nvd3','angularSpinner','ngMaterial'])
.controller('mainNavBarCtrl',function($scope,$location,Notes,$timeout){
    var activeCss = 'activeNavItem';//'nav-link active';
    var inactiveCss = 'nav-link text-white';

    function makeLink(path){
        var obj={};
        obj.path = "/" + path;
        if ($location.path() === obj.path){
            obj.css = activeCss;
        }else{
            obj.css = inactiveCss;
        }        
        return obj;
    }        
    var links = {};
    links[0] = makeLink('main');
    if($location.path() === '/'){
        links[0].css = activeCss;
    }
    links[1] = makeLink('processing');
    links[2] = makeLink('atatData');
    links[3] = makeLink('report');
    links[4] = makeLink('manualMode');
    links[5] = makeLink('logging');
    $scope.links = links;

    $scope.updateSelected = function(viewLocation){
        for (var ctr = 0; ctr < 6; ctr++){
            if(viewLocation === $scope.links[ctr].path){
                $scope.links[ctr].css = activeCss;
            }else{
                $scope.links[ctr].css = inactiveCss;
            }
        }             
    }; 
    $scope.note = "";

    $scope.checkForEnterPress = function(event){

        if ( (event.code === "Enter") && ($scope.note !== "") ){
            makeNote();            
        }        

    }

    $scope.addNote = function(){        
        makeNote();
    }
    function makeNote(){
        var info = {
            note: $scope.note
        }

        Notes.postTimeStampedNote(info).then(function(){
            console.log("note added!");
            $scope.note = "";
            $scope.showFeedback=true;
            $scope.feedback = "Note added.";
            $timeout(function(){
                $scope.feedback = "";
                $scope.showFeedback=false;
            },2500)
        })
    }

})