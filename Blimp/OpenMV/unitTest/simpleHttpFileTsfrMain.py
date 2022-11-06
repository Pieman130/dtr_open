import http_get
import http_update
import hardware
import comms


hw = hardware.Hardware()
comm = comms.Comms(hw)

host = '192.168.1.100:8080'
path = '/'
filename = 'test45.txt'
http_get.http_get(host,path,filename)

filename = 'test4.txt'
http_get.http_get(host,path,filename)
print("done - resetting")
hw.pybReset()
