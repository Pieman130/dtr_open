import evdev
from evdev import InputDevice, categorize, ecodes 
import os
from time import sleep
from gpiozero import Servo, Motor, DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import threading
import sys

#evdev mappings (change these to change controller configuration)
JOY_MAX = 127 #scaling factor to set joystick signals between -1 and 1
YAW = 'ABS_Z'
THRUST = 'ABS_RX'
UP = 'BTN_BASE4'
DOWN = 'BTN_BASE3'
D_FWD = 'BTN_TOP2'
D_BKW = 'BTN_BASE'
D_LFT = 'BTN_BASE2'
D_RGT = 'BTN_PINKIE'

MIN_PW = 0.001148
MAX_PW = 0.001832

#Setup servo and motor signals
motorFL = Servo(7, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=PiGPIOFactory())
motorFR = Servo(1, min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=PiGPIOFactory())
motorAF = Servo(12,min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=PiGPIOFactory())
motorAR = Servo(16,min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=PiGPIOFactory())
motorST = Servo(20,min_pulse_width=MIN_PW, max_pulse_width=MAX_PW, pin_factory=PiGPIOFactory())
servoST = Servo(21, min_pulse_width=.00052, max_pulse_width=.00217,pin_factory=PiGPIOFactory())
#servoST=Servo(21,min_pulse_width=MIN_PW, max_pulse_width=MAX_PW,pin_factory=PiGPIOFactory())
def perform_action(action):
    '''Carry out actions captured from last look at joystick events'''
    #control climb/descend
    if action['climb'] == 1 and action['descend'] == 1:
        motorAF.mid()
        motorAR.mid()
        #servoR.max()
    elif action['descend'] == 1:
        motorAR.min()
        motorAF.min()
        #servoR.min()
    elif action['climb'] == 1:
        motorAR.max()
        motorAF.max()
        #servoR.min()
    elif action['climb'] == 0 or action['descend'] == 0:
        #pass
        motorAR.mid()
        motorAF.mid()
       # servoR.max()
    else:
        motorAR.mid()
        motorAF.mid()
        #servoR.max()

    #control yaw and thrust
    t = action['thrust']
    y = action['yaw']
    if t<-0.1 or t>0.1:#forward or reverse
        motorFL.value = t
        #motorFR.value = -t #NOT USED

        if y>0.1:#thrust and right
            servoST.min()
            motorST.value = y
        elif y<-0.1:#thrust and left
            servoST.max()
            motorST.value = -y
        else: #thrust only
            servoST.mid()
            motorST.mid()
            #motorST.value = t
    elif y>0.1:#only right
        servoST.min()
        motorST.value = y
    elif y<-0.1:#only left
        servoST.max()
        motorST.value = -y
    else: #neutral
        motorFL.mid()
        motorFR.mid()
        servoST.mid()
        motorST.mid()


#loop while waiting for controller to connect
gamepad = False
while not gamepad:
    devices = [InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if device.name[0:15] == 'PLAYSTATION(R)3':
            gamepad = device
            break
    print ("Waiting on PS3 controller connection.")
    sleep(1)

print("Controller Connected.")

action = {'yaw':0,'thrust':0,'climb':0,'descend':0}

def read_joystick(action):
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                if ecodes.ABS[event.code] == YAW:
                    action['yaw']=event.value/JOY_MAX
                elif ecodes.ABS[event.code] == THRUST:
                    action['thrust']=event.value/JOY_MAX
            if event.type == ecodes.EV_KEY:
                try:
                    evnt = ecodes.keys[event.code]
                    if evnt == UP:
                        action['climb'] = event.value
                    elif evnt == DOWN:
                        action['descend'] = event.value
                #D-Pad Mapping to absolute directions
                    elif evnt == D_FWD:
                        if event.value == 1:
                            action['thrust'] = -1
                        else:
                            action['thrust'] = 0
                    elif evnt == D_BKW:
                        if event.value == 1:
                            action['thrust'] = 1
                        else:
                            action['thrust'] = 0
                    elif evnt == D_LFT:
                        if event.value == 1:
                            action['yaw'] = -1
                        else:
                            action['yaw'] = 0
                    elif evnt == D_RGT:
                        if event.value == 1:
                            action['yaw'] = 1
                        else:
                            action['yaw'] = 0
                except KeyError: #unmapped buttons
                    pass

joy = threading.Thread(target=read_joystick, args=(action,))
joy.start()
while(True):
    try:
        perform_action(action)
    except KeyboardInterrupt:
        print ("Quitting....")
        sys.exit()

