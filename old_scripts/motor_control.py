import pygame
import sys
from time import sleep
from gpiozero import Servo, Motor, DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

pygame.init()
joy_count = pygame.joystick.get_count()
servoL = Servo(17, pin_factory=PiGPIOFactory())
motorL = Motor(27,22)
servoR = Servo(10, pin_factory=PiGPIOFactory())
motorR = Motor(9,11)
enable = DigitalOutputDevice(23, initial_value=True)

if joy_count == 0:
    print ("No joysticks found!!")
    pygame.quit()
    sys.exit()

else:
    joy = pygame.joystick.Joystick(0)
    joy.init()

axes = joy.get_numaxes()
but = joy.get_numbuttons()

def getStick(axis):
    if joy.get_axis(axis) < -0.1 or joy.get_axis(axis) > 0.1:
        return axis

def getButton(num):
    if joy.get_button(num):
        return num

def perform_action(action):
    #adjust thrust vector, could also use servo.value(<value>)
    if 3 in action['stick']:
        if 9 in action['button']:
            servoL.min()
            servoR.min()
        elif 8 in action['button']:
            servoL.max()
            servoR.max()
        else:
            servoL.mid()
            servoR.mid()

    #direction: fwd, rev, lft, rgt
    directionL = 0
    directionR = 0

    if 3 in action['stick'] or 2 in action['stick']:
        t = joy.get_axis(3)
        s = joy.get_axis(2)
        if t<-0.1:#forward
            if s>0.1:#forward and right
                motorL.forward(-1*t*s)
                motorR.backward(-1*t*s)
            elif s<-0.1:#forward and left
                motorL.backward(-1*t*-1*s)
                motorR.forward(-1*t*-1*s)
            else: #straight forward
                motorL.forward(-1*t)
                motorR.forward(-1*t)
        elif t>0.1 :#backward
            if s>0.1: #backward and right
                motorL.backward(t*s)
                motorR.forward(t*s)
            elif s<-0.1:#backward and left
                motorL.forward(t*-1*s)
                motorR.backward(t*-1*s)
            else: #straight backward
                motorL.backward(t)
                motorR.backward(t)
        elif s>0.1:#only right
            motorL.forward(s)
            motorR.backward(s)
        elif s<-0.1:#only left
            motorL.backward(-s)
            motorR.forward(-s)
    else: #neutral
        motorL.forward(0)
        motorR.forward(0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    action = {'button':[],'stick':[]}
    if axes !=0:
        for a in range(axes):
            act = getStick(a)
            if act != None:
                action['stick'].append(act)
    if but !=0:
        for b in range(but):
            act = getButton(b)
            if act != None:
                action['button'].append(act)
    print(action)
    perform_action(action)
   # t = input("continue?")




    
