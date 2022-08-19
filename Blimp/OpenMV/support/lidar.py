import mavlink
import time

class Lidar():
    def __init__(self):
        self.mavlink = mavlink.MavLink()
        self.mavlink.send_set_msg_interval_cmd(132,50000)
        print("INITIALIZED")
        time.sleep(0.5)
        
    
    def getData(self):    
        msg = self.mavlink._uart.readline()
        
        if msg != None:
            dist = self.mavlink.parse_distance(msg)
        
        else:
            dist = None
        
        return dist
            