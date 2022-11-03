import rpc
import network
network_if = network.LAN()
network_if.active(True)
network_if.ifconfig('dhcp')
interface = rpc.rpc_network_master(network_if)