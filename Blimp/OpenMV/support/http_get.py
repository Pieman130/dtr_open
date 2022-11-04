import network
import usocket
import urequests

def http_get(host, path, filename):
    response = urequests.get('http://%s%s%s' %(host, path, filename))
    print('getting: http://%s%s%s' %(host, path, filename))
    file = open('/%s'%(filename), "w")
    file.write(response.content)
    file.close()
