 /* ideas and concepts taken from https://github.com/npm/npmlog */

/*
Reset = "\x1b[0m"
Bright = "\x1b[1m"
Dim = "\x1b[2m"
Underscore = "\x1b[4m"
Blink = "\x1b[5m"
Reverse = "\x1b[7m"
Hidden = "\x1b[8m"

FgBlack = "\x1b[30m"
FgRed = "\x1b[31m"
FgGreen = "\x1b[32m"
FgYellow = "\x1b[33m"
FgBlue = "\x1b[34m"
FgMagenta = "\x1b[35m"
FgCyan = "\x1b[36m"
FgWhite = "\x1b[37m"

BgBlack = "\x1b[40m"
BgRed = "\x1b[41m"
BgGreen = "\x1b[42m"
BgYellow = "\x1b[43m"
BgBlue = "\x1b[44m"
BgMagenta = "\x1b[45m"
BgCyan = "\x1b[46m"
BgWhite = "\x1b[47m"
*/

var fs = require('fs').promises;

var colors = {
    'red': '\x1b[31m%s\x1b[0m',
    'green': '\x1b[32m%s\x1b[0m',
    'yellow': '\x1b[33m%s\x1b[0m',
    'blue': '\x1b[34m%s\x1b[0m',
    'magenta': '\x1b[35m%s\x1b[0m',
    'cyan': '\x1b[36m%s\x1b[0m',
    'white': '\x1b[37m%s\x1b[0m'
}

var utility = require('./utilityFcns');
var fileOps = require('./fileOps.js')

function getLogger(isFileLoggingOn = false){    
    //todo: add to verbose level the file written from.
    
    var obj={
        LEVEL_SILENT: 0,
        LEVEL_ERROR: 1,
        LEVEL_WARNING: 2,
        LEVEL_HEARTBEAT: 3,  //for time related things.
        LEVEL_INFO: 4, //normal status messages.        
        LEVEL_VERBOSE: 5, //everything that might be useful.
        LEVEL_SILLY: 6, //crazy debug messages

        level: null,
        write: {},
        callingFcnName: '',
        isFileLoggingOn: isFileLoggingOn,
        loggerStartupTime:  utility.getTimestamp(),
        set logPath(val){
            fileOps.createDirIfNeeded(val)
            obj.logPath_val = val;
        },
        logPath_val: '',
        logFileName: '',
        filePrefix: '',
        logFileNameFullPath(){            
            var filePrefixStr = obj.filePrefix;
            if(obj.filePrefix !== ''){
                filePrefixStr = '_' + filePrefixStr;
            }
            obj.logFileName = "Log_" + obj.loggerStartupTime + filePrefixStr + ".txt";

            return obj.logPath_val + "/" + obj.logFileName;
        },
        /* write methods */
        error(text){
            obj.callingFcnName = utility.getCallingFunctionName();
            let data = {'name':'error','level': obj.LEVEL_ERROR, 'text': text, 'color': colors.red };            
            obj.writeIf(data);
        },
        warning(text){
            obj.callingFcnName = utility.getCallingFunctionName();
            let data = {'name':'warning','level':obj.LEVEL_WARNING, 'text': text, 'color': colors.yellow};    
            obj.writeIf(data);
        },                
        heartbeat(text){
            obj.callingFcnName = utility.getCallingFunctionName();
            let data = {'name':'heartbeat','level':obj.LEVEL_HEARTBEAT, 'text': text, 'color': colors.white};    
            obj.writeIf(data);
        },
        info(text){
            obj.callingFcnName = utility.getCallingFunctionName();
            let data = {'name':'info','level':obj.LEVEL_INFO, 'text': text, 'color': colors.green};   
            obj.writeIf(data);
        },
        verbose(text){
            obj.callingFcnName = utility.getCallingFunctionName();
            let data = {'name':'verbose','level':obj.LEVEL_VERBOSE, 'text': text, 'color': colors.blue};   
            obj.writeIf(data);
        },
        silly(text){
            obj.callingFcnName = utility.getCallingFunctionName();
            let data = {'name':'silly','level':obj.LEVEL_SILLY, 'text': text, 'color': colors.magenta};   
            obj.writeIf(data);
        },
        /* ************ */

        writeIf(data){            
            if(data.level <= obj.level){
                obj.sendToStdout(data);

                if(obj.isFileLoggingOn){
                    obj.sendToFile(data);
                }
            }
        },
        sendToStdout(data){
            if(typeof data.text === 'string'){
                console.log(data.color,data.text.padEnd(80) + " (" + obj.callingFcnName + ")");
            }else{
                obj.warning("LOGGER WARNING: " + obj.callingFcnName + " trying to pass non-string to logger to print");
            }
            
        },
        sendToFile(data){
            var timestamp = utility.getTimestamp();
            var prefix = "[" + timestamp + "]_|" + data.name + "| ";
            var content =  prefix.padEnd(35) + data.text;
            var logText = content.padEnd(110) + " (" + obj.callingFcnName + ") \r\n";
            fs.writeFile(obj.logFileNameFullPath(),logText,{flag: 'a+'},function(){})            
        }        
    }   
    

    //setting default log folder
    var starDataPath = process.env.STARData;    
    if(starDataPath === undefined){
        throw(Error('STARData Environment variable not defined'));
    }
    obj.logPath = starDataPath + '/TestData';    
    
    
    obj.level = obj.LEVEL_SILLY;
    
    return obj;
 }

 module.exports = {
     getLogger: getLogger
 }
