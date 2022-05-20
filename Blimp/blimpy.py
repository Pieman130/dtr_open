import evdev
from evdev import InputDevice, categorize, ecodes 
import os
import sys
from time import sleep, time
from gpiozero import Servo, Motor, DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from attrdict import AttrDict
from collections import namedtuple
import numpy as np
import cv2
from simple_pid import PID
import board
import busio
#import adafruit_bno055 NO LONGER USED
import adafruit_tfmini
import serial
import threading
from flask import Flask, send_file
from subprocess import check_output
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO

sys.path.append('/home/pi/dtr/bno055-python-i2c')
from BNO055 import BNO055

#MIN-MAX Settings for PWM control of ESCs and Servo
MIN_PULSE = 0.001148 #configurable using BLHeli_S ESC firmware uploader
MAX_PULSE = 0.001832
MAX_SERVO = 0.00217 #servo max/min found by trial and error
MIN_SERVO = 0.00052


#evdev mappings (change these to change controller configuration)
ps3 = AttrDict({'name': 'PLAYSTATION(R)3',
                'yaw': 'ABS_Z', 
                'thrust':'ABS_RX', 
                'up':'BTN_BASE4', 
                'down':'BTN_BASE3',
                'forward':'BTN_TOP2', 
                'backward':'BTN_BASE', 
                'left':'BTN_BASE2',
                'right':'BTN_PINKIE', 
                'deadman':'BTN_DEAD',
                'start':'BTN_TOP',
                'ball_captured': 'BTN_JOYSTICK',
                'trap': 'BTN_BASE6'}) #THESE MAPPINGS ARE FOR SONY BRAND PS3 Controller

#State definitions defined by self.state: 
#'in_position','target_located','target_inrange','target_captured','goal_located','goal_inrange', goal_oriented'
#self.state is compared to STATE to determine which state we are in.
STATE = AttrDict({      'READY':(False,False,False,False,False,False,False),
             'SEARCHING_TARGET':(True, False,False,False,False,False,False),
             'MOVING_TO_TARGET':(True, True, False,False,False,False,False),
             'CAPTURING_TARGET':(True, True, True, False,False,False,False),
               'SEARCHING_GOAL':(True, True, True, True, False,False,False),
               'MOVING_TO_GOAL':(True, True, True, True, True, False,False),
            'ORIENTING_TO_GOAL':(True, True, True, True, True, True, False),
                 'SCORING_GOAL':(True, True, True, True, True, True, True )})


class Blimpy():
    def __init__(self, g_color,  #goal color, either orange or yellow depending on which side we are assigned 
                    controller_map=ps3, #Need to add new controller map for evdev if non-PS3 controller used
                    allow_manual = True, #if only using autonomous control set to False (won't block waiting for controller)
                    pic_server = True): #Enables flask server to serve images from main camera
        '''Requires Goal color either "yellow" or "orange" 
        detect functions modify blimpy state vector
        perform functions modify action vector (except for perform_action)'''
        self.exiting = False

        self.loop_time = time()

        self.action = AttrDict({'yaw':0, #Action values provided by manual or autonomous controller
                                'thrust':0,
                                'altitude':0})

        #Setup motor signals for ESC control
        self.thrust_motor =  Servo(7, min_pulse_width=MIN_PULSE, max_pulse_width=MAX_PULSE, pin_factory=PiGPIOFactory())
        self.altitude_fwd =  Servo(12,min_pulse_width=MIN_PULSE, max_pulse_width=MAX_PULSE, pin_factory=PiGPIOFactory())
        self.altitude_rear = Servo(16,min_pulse_width=MIN_PULSE, max_pulse_width=MAX_PULSE, pin_factory=PiGPIOFactory())
        self.yaw_motor =     Servo(20,min_pulse_width=MIN_PULSE, max_pulse_width=MAX_PULSE, pin_factory=PiGPIOFactory())
        self.yaw_servo =     Servo(21,min_pulse_width=MIN_SERVO, max_pulse_width=MAX_SERVO, pin_factory=PiGPIOFactory())

        #self.ready = DigitalOutputDevice(X, initial_value=False) #Allows LED to show when in autonomous mode
        #self.door = Servo(XX, pin_factory=PiGPIOFactory()) #TODO set pin for capture door servo

        #Manual Control settings
        self.manual = controller_map
        self.manual_en = False #enable with dead man switch
        self.joystick = None #joystick object from evdev
        joystick_th = threading.Thread(target=self.joystick_monitor) #starts a thread to constantly read joystick

        #State dictionary
        self.state = AttrDict({'in_position': False, 
                                'target_located': False,
                                'target_inrange': False,
                                'target_captured': False,
                                'goal_located': False,
                                'goal_inrange': False,
                                'goal_oriented': False})
        
        if allow_manual: 
            self.connect_controller()
            joystick_th.start()
        else: #if no controller used assume autonomy starts immediately
            self.state.in_position = True

        #for trap door
        #TODO Add setup stuff for door servo using Servo function
        self.trap_closed = False

        #Camera Settings - using on-board ArduCam 
        self.video = cv2.VideoCapture(0)
        #Mask - Lower and Upper for [Hue, Staturation, Value] 
        #NOTE original green mask was [30,100,50]-[60,255,255]
        self.target_mask = np.array([[50,100,130],[70,255,255]],dtype='uint8') #mask for ball
        if g_color == 'yellow': 
            self.goal_mask = np.array([[25,100,120],[50,255,140]],dtype='uint8') #mask for yellow goal
        elif g_color == 'orange':
            self.goal_mask = np.array([[5,75,120],[20,255,255]],dtype='uint8') #mask for orange goal
        else:
            print("Goal color must be 'yellow' or 'orange'!")
            self.exiting = True
            sys.exit() 
        self.g_color = g_color
        self.current_mask = None #mask of current object of interest

        #PID Settings
        #First 3 parameters in PID are gains: P, I, D #These need to be tuned through experimentation
        #Follow this process for descent tuning results: 
        ######https://robotics.stackexchange.com/questions/167/what-are-good-strategies-for-tuning-pid-loops
        #setpoint is value we are trying to achieve 0.0 represents center pixel of image
        self.pidx = PID(1.5,0.1,8.0, setpoint = 0.0) 
        self.pidy = PID(5.0,0.0,0.00, setpoint = 0.0)
        self.pidx.output_limits = (-1.0, 1.0)
        self.pidy.output_limits = (-1.0, 1.0)
        #PID usage: https://github.com/m-lundberg/simple-pid#usage

        #IMU setup 
        #NOTE Ensure RPI SW I2C bus enabled on GPIO pins 23 & 24
        #i2c = busio.I2C(board.SCL,board.SDA)
        self.IMU = BNO055()
        if self.IMU.begin() is not True:
            print("Error initializing IMU")
            self.exiting = True
            sys.exit()
        self.IMU.setExternalCrystalUse(True)
       

        #Ultrasonic Sonar - setup
        self.trig = 2
        self.echo = 3
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        self.ping_actual = 0.0
        self.sonar_distance = 450 #max range for starting point
        sonar_th = threading.Thread(target=self.measure_sonar) #run sonar in separate thread
        sonar_th.start()

        #TF Mini Lidar - positioned as ceiling sensor
        #NOTE if Lidar not connected serial.Serial will silently block!
        uart = serial.Serial("/dev/ttyS0")
        self.tfmini = adafruit_tfmini.TFmini(uart)
        #TF Mini Usage: https://circuitpython.readthedocs.io/projects/tfmini/en/latest/index.html

        #Picture Server, DISABLE if it makes control loop too slow by setting blimpy param pic_server=False
        self.pic_server = pic_server
        if pic_server:
            self.pic_timer = time()-5.0 #start timer 5seconds ago
            ip = check_output(['hostname', '-I']).decode().split(' ')[0] #get the ip addr of default route
            app = Flask(__name__)

            @app.route("/")
            def path():
                path = "/home/pi/img/"
                img_path = os.path.join(path, "image.jpg")
                return send_file(img_path)

            def picture_server(ip):
                app.run(debug=False, port=5000, host=ip)
            
            pic_srvr = threading.Thread(target=picture_server, args=(ip,)) #starts a thread to constantly read joystick
            pic_srvr.setDaemon(True)
            pic_srvr.start()
        ##End picture server##

        
    def connect_controller(self):
        '''blocks while waiting for controller to connect'''
        while not self.joystick:
            devices = [InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                if device.name[0:15] == self.manual.name:
                    self.joystick = device
                    break
            print ("Waiting on controller connection.")
            sleep(1)
        print("Controller Connected.")


    def joystick_monitor(self):
        '''Function that runs in separate thread to monitor inputs from joystick.
        Called during __init__'''
        print ("Starting Joystick Monitor.")
        while not self.exiting:
            self.read_joystick_event()
        print ("Stopping Joystick Monitor.")


    def read_joystick_event(self,joy_max=127):
        '''Read a single evdev event from joystick.
        joy_max is max value for EV_ABS events'''

        if not self.joystick: #no joystick connected
            return False

        event = self.joystick.read_one()
        if event != None:
            if event.type == ecodes.EV_KEY:
                try:
                    if ecodes.keys[event.code] == self.manual.deadman:
                        if event.value == 1:
                            self.manual_en = True
                            return True
                        else:
                            self.manual_en = False
                            #override actions if deadman released first
                            self.action.yaw = 0
                            self.action.thrust = 0
                            self.action.altitude = 0
                            return False
                    elif ecodes.keys[event.code] == self.manual.start:
                        if event.value == 1: #push start button to signal transition to next state.
                            if self.state.in_position == True:
                                for st_attr in self.state: #if start button pushed again return to READY state
                                    self.state[st_attr] = False
                                #self.state.in_position = False
                                #self.ready.off() #TODO enable if using LED indicator
                            else:
                                self.state.in_position = True
                                #self.ready.on() #TODO enable if using LED indicator
                    elif ecodes.keys[event.code][0] == self.manual.ball_captured:
                         if event.value == 1: #push start button to signal transition to next state.
                            if self.state.target_captured == True:
                                for st_attr in self.state: #if start button pushed again return to READY state
                                    self.state.target_captured = False
                                    self.state.target_located = False
                                    self.state.target_inrange = False
                            else:
                                self.state.target_captured = True
                                self.state.target_located = True 
                                self.state.target_inrange = True
                                self.state.in_position = True
                    elif ecodes.keys[event.code] == self.manual.trap: #controls manual opening and closing of door
                        if event.value == 1:
                            if self.trap_closed == False:
                                self.door.min()
                                self.trap_closed = True 
                            else:
                                self.door.max()
                                self.trap_closed = False
                            print("Trap Closed: ", self.trap_closed)
  
                except KeyError: #Non-mapped button pressed
                    pass #ignore input if non-mapped button pressed
            if self.manual_en:
                if event.type == ecodes.EV_ABS: #for analog sticks, not recommended to use these
                    pass #analog sticks disabled
                elif event.type == ecodes.EV_KEY:
                    try:
                        evnt = ecodes.keys[event.code]
                        if evnt == self.manual.up:
                            self.action.altitude = -event.value
                        elif evnt == self.manual.down:
                            self.action.altitude = event.value
                        #D-Pad Mapping to absolute directions
                        elif evnt == self.manual.forward:
                            if event.value == 1:
                                self.action.thrust = -1
                            else:
                                self.action.thrust = 0
                        elif evnt == self.manual.backward:
                            if event.value == 1:
                                self.action.thrust = 1
                            else:
                                self.action.thrust = 0
                        elif evnt == self.manual.left:
                            if event.value == 1:
                                self.action.yaw = -1
                            else:
                                self.action.yaw = 0
                        elif evnt == self.manual.right:
                            if event.value == 1:
                                self.action.yaw = 1
                            else:
                                self.action.yaw = 0
                    except KeyError: #Non-mapped button pressed
                        pass
                return True

        else:
            return False


    def perform_action(self):
        '''Carry out actions captured from latest iteration of event loop
        Min/Max values for motor is -1/+1.  Control inputs are provided by either joystick or autonomy.'''
        
        if self.action.altitude > 0.1 or self.action.altitude < -0.1: #descend
            self.altitude_fwd.value  = self.action.altitude
            self.altitude_rear.value = -self.action.altitude

        #control altitude
        #if self.action.altitude > 0.1: #descend
        #    self.altitude_fwd.value  = self.action.altitude
        #    self.altitude_rear.value = -self.action.altitude
        #elif self.action.altitude < -0.1: #ascend
        #    self.altitude_fwd.value  = -self.action.altitude
        #    self.altitude_rear.value = self.action.altitude
        else: #neutral
            self.altitude_fwd.mid()
            self.altitude_rear.mid()

        #control thrust (fwd/rev)
        if self.action.thrust <-0.1 or self.action.thrust >0.1:
            self.thrust_motor.value = self.action.thrust
        else:
            self.thrust_motor.mid()

         #control yaw (left/right)
         #NOTE Configuration is set to turn servo in direction of desired turn then use motor speed to control
         ##turning rate
         #NOTE To configure the opposite, reverse commented lines for each section below
        if self.action.yaw > 0.1:#right
            self.yaw_servo.min()
            self.yaw_motor.value = -self.action.yaw
            #self.yaw_servo.value = -y
            #self.yaw_motor.min()
        elif self.action.yaw < -0.1:#left
            self.yaw_servo.max()
            self.yaw_motor.value = self.action.yaw
            #self.yaw_servo.value = y
            #self.yaw_motor.max()
        else: #neutral
            self.yaw_motor.mid()
            self.yaw_servo.mid()
           

    def _generate_mask(self, mask_type):
        '''Captures image and then builds mask based on mask_type'''
        if mask_type == 'target':
            mask = self.target_mask
        elif mask_type == 'goal':
            mask = self.goal_mask

        try:
            ret, self.image = self.video.read()
            
            hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV) #convert to HSV
            return cv2.inRange(hsv,mask[0],mask[1])
        except:
            return None


    def detect_object(self,obj_type):
        '''Take a look to see if we can see either the target or the goal'''
        self.current_mask = self._generate_mask(obj_type)
            
        try:
            contours, hierarchy = cv2.findContours(self.current_mask, cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            largest_blob = max(contours, key=lambda el: cv2.contourArea(el))
            if self.pic_server:
                #if time() - self.pic_timer > 5.0: #TODO uncomment this to only stream image every 5sec
                        image_copy = self.image.copy()
                        cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, 
                            color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                        cv2.drawContours(image=image_copy, contours=largest_blob, contourIdx=-1, 
                            color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                        cv2.imwrite("/home/pi/img/image.jpg", image_copy)
            if cv2.contourArea(largest_blob) > 5.0:
                if obj_type == 'target':
                    self.state.target_located = True 
                elif obj_type == 'goal':
                    self.state.goal_located = True 
                M = cv2.moments(largest_blob)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                err = (int(self.current_mask.shape[1]/2-center[0]), #target is centered in x but top of screen in y
                       int(self.current_mask.shape[0]/20-center[1]))
                self.obj_err = (err[0]/640,err[1]/480) #TODO Confirm this is valid or should it be half this (see below line)
                #self.obj_err = (err[0]/320, err[1]/240)

            else: #if blob not large enough set state to object not located
                if obj_type == 'target':
                    self.state.target_located = False 
                elif obj_type == 'goal':
                    self.state.goal_located = False 
                self.obj_err = None
        except ValueError: #if blob not found set state to object not located
            if obj_type == 'target':
                self.state.target_located = False
            elif obj_type == 'goal':
                self.state.goal_located = False
            self.obj_err = None


    def _get_distance(self):
        '''Reads distance from TFmini lidar.  Currently only used to maintain altitiude.
        Experiments show it is not reliable for detecting objects.'''
        try:
            distance = self.tfmini.distance
        except RuntimeError: #occasional serial timing error 
            try: #try reading lidar again
                distance = self.tfmini.distance
            except:
                distance = 1200 #if no distance returned again assume it is max distance
        return distance


    def _get_yaw(self):
        '''euler values from IMU are the KF filtered values'''
        try:
            #y = self.IMU.euler[0]
            y = bno.getVector(BNO055.VECTOR_EULER)[0]
        except:
            y = None
        return y
    #TODO - other IMU values? Pitch? Roll?


    def _get_sonar(self):
        '''Triggers ultrasonic sensor and waits for return'''
        GPIO.output(self.trig,True)
        sleep(0.00001)
        GPIO.output(self.trig,False)
        start = time()
        stop = time()
        fail = time()
        fail_trigger = False #if return not received, keeps from hanging
        while GPIO.input(self.echo) == 0:
            start = time()
            fail_trigger = False
            if time() - fail > 0.1:
                fail_trigger = True 
                break
        while GPIO.input(self.echo) == 1:
            if fail_trigger == True:
                break
            stop = time()

        elapsed = stop - start 
        dis = (elapsed * 34300)/2 #distance in cm (for inches use 13400)

        return dis


    def measure_sonar(self):
        '''Use in conjunction with _get_sonar to get a stabilized distance reading from sonar.
        Run as a separate thread to better control timing'''
        dv = [] #distance vector
        prev_dist = 0.0 #smooth out errors in echo
        while True:
            d = self._get_sonar()
            if len(dv) < 10:
                dv.append(d)
            else:
                dv.pop(0) #keep the distance vector no larger than last 10 measurements
                dv.append(d)

            if len(dv) >= 10:
                int_dist = ([int(x) for x in dv]) #convert distance vector to integer values
                mode_dist = max(set(int_dist),key=int_dist.count) #find mode of last 10 measurements
                if mode_dist > 450:
                    mode_dist = prev_dist
                prev_dist = mode_dist
                self.sonar_distance = mode_dist


    def detect_target_in_range(self):
        '''If sonar detects object within 2ft range it sets state to target in range
        TODO Probably need to adjust this since this is just an initial guess'''
        if self.sonar_distance < 60: #target in range when within 60cm (2ft)
            self.state.target_inrange = True 
        else:
            self.state.target_inrange = False


    def detect_target_captured(self):
        '''If sonar detects object within range it sets state to target in range
        TODO Realistically this process will probably be much more complicated, but 
        maybe not?'''
        if self._get_distance() < 5:
            self.state.target_captured = True 
            #self.state.target_captured = False
        else:
            self.state.target_captured = False


    def detect_goal_in_range(self):
        '''Determine if we are close enough to the goal to perform fine maneuver
        to get us in position to score.
        TODO Is this the same as detect_target_in_range?'''
        if self.sonar_distance < 60: #target in range when within 60cm (2ft)
            self.state.target_inrange = True 
        else:
            self.state.target_inrange = False

    def detect_goal_oriented(self):
        '''Determine if we are properly oriented to the goal so we can get the 
        ball through the goal'''
        #TODO what do we do to detect if we are in the right position to score??
        correct_position = False #place holder, how do we determine correct position
        if correct_position:
            self.state.goal_oriented = True 
        else:
            self.state.goal_oriented = False


    def perform_search_for_object(self,obj_type):
        '''Perform search pattern for objects, counter-clockwise helical pattern
        Pattern repeats based on self.pattern_time'''
        #TODO Determine search pattern by controlling thrust, yaw, and altitude
        #COARSE MANEUVER
        self.action.yaw = 0 #TODO REMOVE!!!
        #output is to self.action
        pass
   

    def perform_move_to_object(self,object):
        '''uses self.obj_err and PID control to guide blimpy towards object.  
        Part of the problem we found early on is for blimps when you stop the 
        control input it doesn't stop the motion of the blimp.  For example if 
        you start turning, it doesn't stop turning because you turned the motor 
        off.  You will need to provide a control input to counter the momentum from
        the last command.'''
        
        #Feed error from object detection into PID to get dampened control input
        #obj_err is a tuple (Err_x,Err_y)
        resultx = self.pidx(self.obj_err[0])
        resulty = self.pidy(self.obj_err[1])
        print("X: ", resultx, "Y:", resulty, "based on error of: ", self.obj_err)

        #PID output in the x direction
        self.action.yaw = resultx
        
        #PID output in the y direction
        self.action.climb = resulty
      
        #TODO What about thrust?
     
        #output is to self.action


    def perform_orient_to_goal(self):
        '''Once in range of goal perform movements to get ball through goal.  This is
        a fine maneuver action to align blimp so it can get ball through the goal instead
        of crashing into the side or something.'''
   
        #TODO determine fine maneuvers 
        #TODO Should this include moving through the goal?
        self.action.yaw = 0 #TODO REMOVE!!!
        pass
        #output is to self.action


    def perform_target_capture(self):
        '''Once target is in range perform fine movements to ensure ball is captured.  
        Could include operating the capture door.'''
        #FINE MANEUVER
        #TODO determine fine maneuvers operating the door?
        self.action.yaw = 0 #TODO REMOVE!!!
        pass
        #output is to self.action


    def observe_orient_decide(self):
        '''Makes observations, determines current state, decides the appropriate action based
        on current state.  This is the primary function that determines what we should do next.
        The CONTROL FLOW is:

        1) Check if we are in manual or autonomous mode (Operator presses <START> button) 
            a)If in manual (READY STATE) perform action given by joystick input (running in separate thread), end of the loop.
            b)If in autonomous mode (any other state than READY STATE) check what state we are in, goto (2)
        2) Check if the ball has been captured 
            a) If ball has been captured we check to see if we are in position to score, goto (3)
            b) If ball has NOT been captured we need to look for the ball, goto (4)
        3) If ball has been captured check to see if we are in position to score
            a) If we are in position to score we need to do something to score (TBD), end of the loop
            b) If we are NOT in position we need to check if we can see the goal, goto (5)
        4) If ball has not been captured check if it is in close enough range to try and capture it (about 2ft)
            a) If it is in range maneuver the blimp to capture the ball, end of the loop
            b  If it is NOT in range, check if we see the ball with the camera, goto (6)
        5) If the ball has been captured, but we not in position to score, check if we can see the goal
            a) If we can see goal, check if we are in close range to the goal, goto (7)
            b) If we can't see the goal, we need to search for the goal, end of the loop 
        6) If the ball has not been captured, and it is not in range, check if we can see the ball with the camera
            a) If we can see the ball we need to maneuver towards it, end of the loop
            b) If we can't see the ball we need to search for it, end of loop 
        7) If the ball has been captured and we can see the goal, check if we are close range to the goal
            a) If we are in close range to goal, orient ourselves in position to score, end of loop
            b) If we are not in close range to the goal, move towards the goal, end of loop'''
        start = time()
        if self.state.in_position == True:
            self.detect_target_captured()
            if self.state.target_captured == True:
                self.detect_goal_oriented()
                if self.state.goal_oriented == True:
                    #TODO what do we do here?  Wait for manual or just move forward, release door, etc.?
                    pass
                else:
                    self.detect_object('goal')
                    if self.state.goal_located == True:
                        self.detect_goal_in_range()
                        if self.state.detect_goal_in_range == True:
                            self.perform_orient_to_goal()
                        else:
                            self.perform_move_to_object('goal')
                    else:
                        self.perform_search_for_object('goal')
            else:
                self.detect_target_in_range()
                if self.state.target_inrange == True:
                        self.perform_target_capture()
                else:
                    self.detect_object('target')
                    if self.state.target_located == True:
                        self.perform_move_to_object('target')
                    else:
                        self.perform_search_for_object('target')
        self.loop_time = time() - time()              
        

if __name__ == '__main__':
    if len(sys.argv) == 2:
        g_color = sys.argv[1] #goal color should be the only CL input
    else:
        print("Missing Goal Color!")
        sys.exit()
    blimpy = Blimpy(g_color, pic_server=False)
    dt = time()
    while not blimpy.exiting: #this is the main control loop

        try:
            blimpy.observe_orient_decide() # The observe, orient, and decide portion of the loop

            #Print current state to screen once per second
            for state in STATE:
                if tuple(blimpy.state.values()) == STATE[state]:
                    if time() - dt > 1.0:
                        print("Distance to Ceiling: ", blimpy._get_distance())
                        print("Sonar distance: ", blimpy.sonar_distance)
                        print("State: ", state)
                        print("Control Loop Time: ", blimpy.loop_time, "seconds")
                        dt = time()

            blimpy.perform_action() #The act portion of the loop

        except KeyboardInterrupt:
            blimpy.exiting = True
            GPIO.cleanup()
            print("Blimpy Exiting!!")
