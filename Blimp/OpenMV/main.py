# Main - By: timothy.woodbridge - Fri May 20 2022

# POWERED UP initializing = 'purple'
# OK, connected to ground station = 'green'
# OK, Not connected to gnd station = 'lightGreen'         
# FAIL 'red'

import sys
import os
import io
import mainWorker

import openMvSwUpdater
import hardware
import comms
import time

host = '192.168.1.100:7071'

def main() -> None:
    try:
        mainWorker.run()

        print(" NEW UPLOAD CODE REQUEST")
        hw = hardware.Hardware()
        comm = comms.Comms(hw)

        runUpdater(hw)
       

    except Exception as e:            

        #buf = io.StringIO()
        #sys.print_exception(e, buf)
        #val = buf.getvalue()
        val = get_exception(e)
        print(type(val))
        #print("I CAUGHT THE ERROR!" + val)

        #print(dir(e))
        #print('err no: ' + e.errno)
        print("Error trying to run main worker: {}".format(e))

    finally:                

        while(True):                    
            time.sleep(1)
            print("Code broken.  Waiting for command to upload fixed code")


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


    print("DONE - RESETTING!")
    time.sleep(5)
    hw.pybReset()


def postUploadStatus(status):
    print("in post upload status fcn")
    pathUpdateStatus = '/updater/updateStatus/'       
    openMvSwUpdater.updateStatus(host,pathUpdateStatus,status)

main()






