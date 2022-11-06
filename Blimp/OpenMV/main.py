# Main - By: timothy.woodbridge - Fri May 20 2022

# POWERED UP initializing = 'purple'
# OK, connected to ground station = 'green'
# OK, Not connected to gnd station = 'lightGreen'         
# FAIL 'red'

import sys
import os
import io
import mainWorker
import json

import openMvSwUpdater
import hardware
import comms
import time

host = '192.168.1.100:7071'
isRunTimeFail = False

def main() -> None:
    try:
        
        mainWorker.run()

        print(" NEW UPLOAD CODE REQUEST")                

        hw = hardware.Hardware()
        comm = comms.Comms(hw)
               
        runUpdater(hw)
        
    except Exception as e:            

        hw = hardware.Hardware()
        comm = comms.Comms(hw)

        #buf = io.StringIO()
        #sys.print_exception(e, buf)
        #val = buf.getvalue()
        #val = get_exception(e)
       # print(type(val))
        #print("I CAUGHT THE ERROR!" + val)

        #print(dir(e))
        #print('err no: ' + e.errno)
        errStr = "Error: {}".format(e)
        print(errStr)

        postRuntimeError(errStr)
        
        while(True):                    
            time.sleep(1)
            print("Code broken.  Waiting for command to upload fixed code")
            r = isUploadRequested()
            print(r)
                        
            if(r['isUploadRequested']):      
                print("request for code update!")      
                runUpdater(hw)
        


def get_exception(err) -> str:
        buf = io.StringIO()
        sys.print_exception(err, buf)
        return buf.getvalue()

def runUpdater(hw):
    path = '/updater/supportFiles'
    resp = openMvSwUpdater.http_getFolderList(host,path)

    path = '/updater/file/'
    
    print("about to update status")
    #status = "Found " + len(resp) + " files in /support folder.  Beginning upload!"
    postUploadStatus('Upload started.')

    for filename in resp:
        print(filename)
       # 
        openMvSwUpdater.getAndUpdateFile(host,path,filename)

    postUploadStatus('Upload complete.  Resetting.')    

    markUploadComplete()

    print("DONE - RESETTING!")
    time.sleep(5)
    hw.pybReset()


def postUploadStatus(status):   
    pathUpdateStatus = '/updater/updateStatus/'       
    openMvSwUpdater.updateStatus(host,pathUpdateStatus,status)

def postRuntimeError(runTimeError):
    pathUpdateStatus = '/updater/openMvRuntimeError/'           
    openMvSwUpdater.postRuntimeError(host,pathUpdateStatus,runTimeError)

def isUploadRequested():
    pathIsUploadRequested = '/updater/updateComplete/'
    r = openMvSwUpdater.isUploadRequested(host,pathIsUploadRequested)
    return r

def markUploadComplete():
    print("about to mark upload complete 1")
    pathUploadComplete = '/updater/markUploadComplete/'
    openMvSwUpdater.markUploadComplete(host,pathUploadComplete)

main()






