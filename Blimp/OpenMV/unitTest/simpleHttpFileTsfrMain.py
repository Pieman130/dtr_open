import http_get
import http_update
import hardware
import comms
import time

hw = hardware.Hardware()
comm = comms.Comms(hw)

#host = '192.168.1.100:8080'
#path = '/'

host = '192.168.1.100:7071'
path = '/updater/file/'
#filename = 'test45.txt'

print("connected!")


filename = 'groundStationTEST.py'
http_get.http_get(host,path,filename)
print('got ground station test')

filename = 'test4.txt'
http_get.http_get(host,path,filename)
print('got test4')


filename = 'test45.txt'
http_get.http_get(host,path,filename)
print('got test4')

print("DONE - RESETTING!")
time.sleep(5)
hw.pybReset()



