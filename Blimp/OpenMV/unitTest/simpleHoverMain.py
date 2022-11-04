import time
import hardware

import pyb
import dataClasses

from machine import Pin
IR_DETECT_PIN = 'P6'
irSensor = Pin(IR_DETECT_PIN,Pin.IN,Pin.PULL_NONE)

UART_BAUDRATE = 115200
UART_TIMEOUT = 1000


HW_UART = 3
class Controls:
    def __init__(self):
        self.yaw = 0  # -1 to 1
        self.up = 0  # -1 to 1
        self.throttle = 0  # -1 to 1
        self.servo = 0  # 0 for OFF. 1 for ON.

class SimpleHw:
    def __init__(self):
        self.uart = pyb.UART(HW_UART)
        self.uart.init(UART_BAUDRATE, timeout=UART_TIMEOUT, bits=8, parity=None, stop=1, flow=0, read_buf_len=64)

    def openDoor(self):
        pass
    def closeDoor(self):
        pass

class SimpleComms:
    def __init__(self,mavlink):
        self.mavlink = mavlink

hw = SimpleHw()

#UART_BAUDRATE = 115200
#UART_TIMEOUT = 1000
#HW_UART = 3
#import pyb
#uart = pyb.UART(HW_UART)
#uart.init(UART_BAUDRATE, timeout=UART_TIMEOUT, bits=8, parity=None, stop=1, flow=0) #, read_buf_len=64)

led = hardware.Led()
import mavlink
import logger
logger.log.setLevel_verbose()

mav = mavlink.MavLink(hw)
comms = SimpleComms(mav)

ctrl = Controls()
r = hw.uart.readline()
print(r)

import flightActions

hoverExit = flightActions.ExitCriteria()
hoverCtrls = flightActions.Controls()

hover = flightActions.FlightAction("hover",hoverCtrls,hoverExit,comms,hw)

dataClasses.config.isMicroPython = True
dataClasses.gndStationCmd.p_up = 1
dataClasses.gndStationCmd.error_rounding_up = 1
dataClasses.gndStationCmd.error_scaling_up = 100
dataClasses.gndStationCmd.pid_min_up = 0
dataClasses.gndStationCmd.scalar_up = 1


while(True):


    time.sleep(0.2)
    
    hover.execute_assisted_altitude(1400)
    current_raw_sensor_data = mav.getSensors() 
    
    if current_raw_sensor_data['Lidar'] != None:
        lidarData = current_raw_sensor_data['Lidar']
        print(str(lidarData))
        dataClasses.data.lidarDistance = lidarData
    

    


    #led.turnOn('blue')
    #print("led blue")
    #ctrl.up = 0.5
    #mav.setControls(ctrl)

   # r = hw.uart.readline()
   # print(r)

    #time.sleep(0.2)
    #led.turnOn('green')
    #print("led green")
    #ctrl.up = -0.5
    #mav.setControls(ctrl)

   # r = hw.uart.readline()
  #  print(r)
