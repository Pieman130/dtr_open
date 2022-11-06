import http_get
import hardware
import comms
import time

hw = hardware.Hardware()
comm = comms.Comms(hw)

#host = '192.168.1.100:8080'
#path = '/'

host = '192.168.1.100:7071'


print("connected!")

path = '/updater/supportFiles'
resp = http_get.http_getFolderList(host,path)


path = '/updater/file/'
for filename in resp:
    print(filename)
    http_get.http_get(host,path,filename)


print("DONE - RESETTING!")
time.sleep(5)
hw.pybReset()





