import ftp
import rpc
import time
ssid = 'DTR_team_a'
key = 'GoBigRed'
#ip = '192.168.1.100'

import network

print(network.STA_IF)

network_if = network.WLAN(network.STA_IF)
network_if.active(True)
network_if.connect(ssid, key)
interface = rpc.rpc_network_slave(network_if)
#interface = rpc.rpc_network_slave(ssid, key)

def doTestPrint():
    print('=======TEST=======')

interface.register_callback(doTestPrint)

while(True):
    time.sleep(0.5)
    print('looping')