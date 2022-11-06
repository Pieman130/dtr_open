import network
import usocket
import urequests

def http_get(host, path, filename):
    print("in http get")
    fullPath = 'http://%s%s%s' %(host, path, filename)
    print(fullPath)
    response = urequests.get(fullPath)
    print(response)
 #   print('getting: http://%s%s%s' %(host, path, filename))
    print("opening file: " + filename)
    file = open('/%s'%(filename), "w")
    print("about to write file")
    print("CONTENT: " + response.content)
    file.write(response.content)
    print("done saving")
    file.close()
    