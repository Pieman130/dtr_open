import network
import usocket
import urequests

def http_getFolderList(host,path):
    fullPath = 'http://%s%s' %(host, path)    
    response = urequests.get(fullPath)
    jsonResp = response.json()    

    return jsonResp

def getAndUpdateFile(host, path, filename):    
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
    data = '{"runTimeError":"' + runTimeErrorJson + '"}'
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