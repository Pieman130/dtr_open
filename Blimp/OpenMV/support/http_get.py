import network
import usocket
import urequests

def http_getFolderList(host,path):
    fullPath = 'http://%s%s' %(host, path)
    print("path: " + fullPath)
    response = urequests.get(fullPath)
    jsonResp = response.json()
    print("response success")

    return jsonResp

def http_get(host, path, filename):
    print("in http get")
    fullPath = 'http://%s%s%s' %(host, path, filename)    
    response = urequests.get(fullPath)     
    print("opening file to write: " + filename)
    file = open('/%s'%(filename), "w")    
    file.write(response.content)
    print("done saving")
    file.close()
    