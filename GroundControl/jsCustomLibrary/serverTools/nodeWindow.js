var handleCloseWindow = function(exitCleanlyFcn){
// be sure to call process.exit(1); after you are finished cleaning up in the "exitCleanlyFcn" function so the process exits.   
 
        process.on("SIGINT",function(){ //catch ctrl+c   
            exitCleanlyFcn();                     
        })   
        process.on("SIGHUP",function(){ //catch window close
            exitCleanlyFcn();
        })          
}
module.exports = { 
    handleCloseWindow: handleCloseWindow
}