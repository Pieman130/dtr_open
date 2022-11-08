import network
import usocket
import urequests
import sys
import io

def http_getFolderList(host,path):
    fullPath = 'http://%s%s' %(host, path)    
    response = urequests.get(fullPath)
    jsonResp = response.json()    

    return jsonResp

def getAndUpdateFile(host, path, filename): 
    if(filename == '__pycache__'):
        print("not uploading pycache")
        return
    else:       
        fullPath = 'http://%s%s%s' %(host, path, filename)    
        response = urequests.get(fullPath)     
        print("opening file to write: " + filename)
        file = open('/%s'%(filename), "w")    
        file.write(response.content)    
        file.close()

def updateStatus(host,path,filename):    
    print("in update status sw fcn")
    fullAddress = 'http://%s%s' %(host, path)    
    print("about to post to: " + str(fullAddress))
    data = '{"updateStatus":"' + filename + '"}'
    print("data: " + data)
    headers = {'Content-Type': 'application/json'}    
    r = urequests.post(fullAddress,data = data,headers = headers)            
    
def postRuntimeError(host,path,runTimeErrorJson):
    print("in post runtime eror function")
    fullAddress = 'http://%s%s' %(host, path)    
    print("about to post to: " + str(fullAddress))
    data = '{"runTimeError":"' + str(runTimeErrorJson) + '"}'
    print("data: " + data)
    headers = {'Content-Type': 'application/json'}    
    r = urequests.post(fullAddress,data = data,headers = headers)            
    
def isUploadRequested(host,path):
    fullPath = 'http://%s%s' %(host, path)    
    response = urequests.get(fullPath)     
    jsonResp = response.json()       
    return jsonResp

def markUploadComplete(host,path):
    print("about to mark upload complete 2")
    fullAddress = 'http://%s%s' %(host, path)    
    print("about to post to: " + str(fullAddress))
    txt = 'nonsense'
    data = '{"nonsense":"' + txt + '"}'    
    headers = {'Content-Type': 'application/json'}    
    r = urequests.post(fullAddress,data = data,headers = headers)   

def exceptionToStr(e):
    #errStr = "Error: {}".format(e)
    #return errStr

    #martin changes:

    buf = io.StringIO()
    sys.print_exception(e, buf)
    #print(buf.getvalue())
    return buf.getvalue()



    #errStr = sys.print_exception(e)
    #print(errStr)
    #print("after print")
    #attr , mod, tr = sys.exc_info()      
    #errStr = mod.args[0] + ", lineno: " + str(tr.tb_lineno)
    #return errStr
