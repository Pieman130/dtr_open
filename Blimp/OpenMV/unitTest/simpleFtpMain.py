print("in main")

import hardware
import comms
import ftp


hw = hardware.Hardware()
comm = comms.Comms(hw)

print("before start ftp server")
port = 21
timeout=None
ftp.ftpserver(port,timeout,comm.wifi.wlan)
print("after start ftp server")

#ftp.start(PORT,VERBOSITY)