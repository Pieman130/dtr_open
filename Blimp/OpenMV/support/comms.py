import mavlink
import urequests

class WiFi:
    def __init__(self,hw):
        self.ssid = 'DTR_team_a'
        self.key = 'GoBigRed'
        self.ip = '192.168.1.100'
        self.wlan = hw.wlan
        self.connect()

    def connect(self):
        self.wlan.connect(self.ssid,self.key)

    def getFullAddress(self,addr: str, api: str) -> str:        
        return 'http://{}:1111/{}'.format(addr, api)

    def post(self,fullAddress,data,headers):
        r = urequests.post(fullAddress,data = data,headers = headers)
        return r


class Comms:
    def __init__(self,hw):
        self.mavlink = mavlink.MavLink(hw)
        self.wifi = WiFi()              