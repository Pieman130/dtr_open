print("in main")

import hardware
import comms
import ftp
import pyb
import test



hw = hardware.Hardware()
comm = comms.Comms(hw)

test.lights()

print("before start ftp server")
port = 21
timeout=None
ftp.ftpserver(port,timeout,comm.wifi.wlan)
print("after start ftp server")

pyb.hard_reset()
#ftp.start(PORT,VERBOSITY)