import evdev
from evdev import InputDevice, categorize, ecodes 
import os
import sys
from time import sleep, time
from gpiozero import Servo, Motor, DigitalOutputDevice
#from gpiozero.pins.pigpio import PiGPIOFactory
from attrdict import AttrDict
from collections import namedtuple
import numpy as np
import cv2
from simple_pid import PID
import board
import busio
import adafruit_bno055
import pupil_apriltags
import adafruit_tfmini
import serial
import threading
from flask import Flask, send_file
from subprocess import check_output
from gpiozero.pins.pigpio import PiGPIOFactory


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

#States
STATE = AttrDict({     'READY':(False,False,False,False,False,False,False),
             'SEARCHING_TARGET':(True, False,False,False,False,False,False),
             'MOVING_TO_TARGET':(True, True, False,False,False,False,False),
             'CAPTURING_TARGET':(True, True, True, False,False,False,False),
               'SEARCHING_GOAL':(True, True, True, True, False,False,False),
               'MOVING_TO_GOAL':(True, True, True, True, True, False,False),
               'ORIENTING_TO_GOAL':(True, True, True,True,True,True,False),
                  'SCORED_GOAL':(True, True, True, True, True, True, True )})


class Blimpy():
    def __init__(self, g_color, lm=(27,22), rm=(9,11), bm=(25,8), am=(23,24), enb1=17, enb2=18,
                    sl =(26,19), sr=(6,5), enb3=13, #TODO input right pins for 3rd motor controller 
                    controller_map=ps3, 
                    allow_manual = True, pic_server = True):
        '''Requires Goal color either "yellow" or "orange" '''
        self.exiting = False

        self.action = AttrDict({'yaw':0,
                                'thrust':0,
                                'climb':0,
                                'descend':0})

        #Setup motor signals FOR USE WITH DRV8833 Dual H-bridge
        self.am = Motor(am[0], am[1])
        self.lm = Motor(lm[0],lm[1])
        self.bm = Motor(bm[0], bm[1])
        self.rm = Motor(rm[0],rm[1])
        self.sl = Motor(sl[0], sl[1])
        self.sr = Motor(sr[0],sr[1])
        self.enable1 = DigitalOutputDevice(enb1, initial_value=True)
        self.enable2 = DigitalOutputDevice(enb2, initial_value=True)
        self.enable3 = DigitalOutputDevice(enb3, initial_value=True)
        self.ready = DigitalOutputDevice(7, initial_value=False)
        self.ready = DigitalOutputDevice(12, initial_value=False)
        self.door = Servo(21, pin_factory=PiGPIOFactory())
        self.door = Servo(16, pin_factory=PiGPIOFactory())

        #For testing Brushless dc motors
        #self.up1 = Servo(16, pin_factory=PiGPIOFactory())
        #self.up2 = Servo(12, pin_factory=PiGPIOFactory())

        #Manual Control settings
        self.manual = controller_map
        self.manual_en = False #enable with dead man switch
        self.joystick = None #joystick object from evdev
        joystick_th = threading.Thread(target=self.joystick_monitor) #starts a thread to constantly read joystick

        #States
        self.state = AttrDict({'in_position': False, 
                                'target_located': False,
                                'target_inrange': False,
                                'target_captured': False,
                                'goal_located': False,
                                'april_detected': False,
                                'goal_achieved': False})

        #for trap door
        self.trap_closed = False

        if allow_manual: 
            self.connect_controller()
            joystick_th.start()
        else: #if no controller used assume autonomy starts immediately
            self.state.in_position = True

        #Search Settings
        self.radius = 2000 #radius of search pattern in mm
        self.length = 400 #distance between motors in mm
        self.pattern_time = 120 #time to perform search pattern (sec)
        self.pattern_state = None
        self.pattern_timer = 0.0
        self.search_up_timer = 0.0
        self.alt_err = 0
        self.srch_prev_act = None
        self.yaw_correction_tmr = 0.0
        self.yaw_correction = False
        self.alt_correct = False
        self.lidar_list = []

        #Camera Settings
        self.video = cv2.VideoCapture(0)
        #Mask - Lower and Upper for [Hue, Staturation, Value] 
        #NOTE original green mask was [30,100,50]-[60,255,255]
        self.target_mask = np.array([[50,100,130],[70,255,255]],dtype='uint8') #TODO Adjust HSV values: 20 is getting into yellow
        if g_color == 'yellow': 
            self.goal_mask = np.array([[25,100,120],[50,255,140]],dtype='uint8')
        elif g_color == 'orange':
            self.goal_mask = np.array([[5,75,120],[20,255,255]],dtype='uint8')
        else:
            print("Goal color must be 'yellow' or 'orange'!")
            self.exiting = True
            sys.exit() 
        self.g_color = g_color
        self.current_mask = None #mask of current object of interest
        self.image_array = [] #holds multiple images
        self.max_len_images = 1

        #PID Settings
        self.pidx = PID(1.5,0.1,8.0, setpoint = 0.0) #(gains: P, I, D)
        self.pidy = PID(5.0,0.0,0.00, setpoint = 0.0)
        self.pidx.output_limits = (-1.0, 1.0)
        self.pidy.output_limits = (-1.0, 1.0)
        #PID usage: https://github.com/m-lundberg/simple-pid#usage

        #IMU setup
        i2c = busio.I2C(board.SCL,board.SDA)
        self.IMU = adafruit_bno055.BNO055_I2C(i2c)
        #IMU usage: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/python-circuitpython#circuitpython-and-python-usage-2974413-15

        #April Tag Detector
        self.april_detector = pupil_apriltags.Detector()
        #April Detector usage: https://github.com/pupil-labs/apriltags#usage

        #TF Mini Lidar
        uart = serial.Serial("/dev/ttyS0")
        self.tfmini = adafruit_tfmini.TFmini(uart)
        #TF Mini Usage: https://circuitpython.readthedocs.io/projects/tfmini/en/latest/index.html

        #Picture Server DISABLE if it makes control loop too slow
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
                    #print("KEY: ", ecodes.keys[event.code])
                    if ecodes.keys[event.code] == self.manual.deadman:
                        if event.value == 1:
                            self.manual_en = True
                            return True
                        else:
                            self.manual_en = False
                            #override actions if deadman released first
                            self.action.yaw = 0
                            self.action.thrust = 0
                            self.action.descend = 0
                            self.action.climb = 0
                            return False
                    elif ecodes.keys[event.code] == self.manual.start:
                        if event.value == 1: #push start button to signal transition to next state.
                            if self.state.in_position == True:
                                for st_attr in self.state: #if start button pushed again return to READY state
                                    self.state[st_attr] = False
                                #self.state.in_position = False
                                self.ready.off()
                            else:
                                self.state.in_position = True
                                self.ready.on()
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
                    elif ecodes.keys[event.code] == self.manual.trap:
                        if event.value == 1:
                            if self.trap_closed == False:
                                self.door.min()
                                self.trap_closed = True 
                            else:
                                self.door.max()
                                self.trap_closed = False
                            print("Trap Closed: ", self.trap_closed)
  
                except KeyError: #Non-mapped button pressed
                    pass
            if self.manual_en:
                if event.type == ecodes.EV_ABS: #for analog sticks, no longer used
                    pass
                elif event.type == ecodes.EV_KEY:
                    try:
                        evnt = ecodes.keys[event.code]
                        if evnt == self.manual.up:
                            self.action.climb = event.value
                        elif evnt == self.manual.down:
                            self.action.descend = event.value
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
        Min/Max values for motor is -1/+1'''
        
        if self.action.descend != 0 and self.action.climb == 0:
            self.am.backward(self.action.descend)
            self.bm.backward(self.action.descend)
            #self.up1.min()
            #self.up2.min()
        elif self.action.climb != 0 and self.action.descend == 0:
            self.am.forward(self.action.climb)
            self.bm.forward(self.action.climb)
            #self.up1.max()
            #self.up2.max()
  
        else:
            self.am.forward(0)
            self.bm.forward(0)
            #self.up1.min()
            #self.up2.min()

        #print("Up Value: ", self.up1, self.up2)
        #control yaw and thrust
        t = self.action.thrust
        y = self.action.yaw
        if t<-0.1:#forward
            self.lm.forward(-t)
            self.rm.forward(-t)
        elif t>0.1 :#backward
            self.lm.backward(t)
            self.rm.backward(t)
        else:
            self.lm.forward(0)
            self.rm.forward(0)

        if y>0.1:#steer right
            self.sr.forward(y)
            self.sl.forward(0)
        elif y<-0.1:#steer left
            self.sr.forward(0)
            self.sl.forward(-y)
        else:
            self.sl.forward(0)
            self.sr.forward(0)
           

    def detect_goal_scored(self):
        '''Need something to declare goal scored
        How the heck do we determine if we scored?  Maybe we don't because the game is over?'''
        goal_scored = False
        #Put something here that detects the goal scoring, or manual (e.g. push a button on controller?)
        if goal_scored == True:
            self.state.goal_achieved = True


    def _generate_mask(self, mask_type):
        '''Takes several images, averages them together and then builds mask'''
        ##start = time()
        if mask_type == 'target':
            mask = self.target_mask
        elif mask_type == 'goal':
            mask = self.goal_mask

        try:
            ret, self.avg_image = self.video.read()
            
            hsv = cv2.cvtColor(self.avg_image,cv2.COLOR_BGR2HSV) #convert to HSV
            #print("Time: ", time()-start)
            return cv2.inRange(hsv,mask[0],mask[1])
        except:
            return None


    def detect_object(self,obj_type):
        '''Take a look to see if we can see either the target or the goal'''
        self.current_mask = self._generate_mask(obj_type)
        old_obj_detect = self.state.target_located
        old_goal_detect = self.state.goal_located
            
        try:
            contours, hierarchy = cv2.findContours(self.current_mask, cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            largest_blob = max(contours, key=lambda el: cv2.contourArea(el))
            if self.pic_server:
                #if time() - self.pic_timer > 5.0:
                        image_copy = self.avg_image.copy()
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
                self.obj_err = (err[0]/640,err[1]/480)
                #self.obj_err = (err[0]/320, err[1]/240)

            else:
                if obj_type == 'target':
                    self.state.target_located = False 
                elif obj_type == 'goal':
                    self.state.goal_located = False 
                self.obj_err = None
        except ValueError:
            if obj_type == 'target':
                self.state.target_located = False
            elif obj_type == 'goal':
                self.state.goal_located = False
            self.obj_err = None

        if old_obj_detect == True and self.state.target_located == False:
            self.lidar_list = []
        elif old_goal_detect == True and self.state.goal_located == False:
            self.lidar_list = [] 

    def _get_distance(self):
        try:
            distance = self.tfmini.distance
        except RuntimeError:
            try:
                distance = self.tfmini.distance
            except:
                distance = 1200
        return distance


    def _get_yaw(self):
        try:
            y = blimpy.IMU.euler[0]
        except:
            y = None
        return y


    def detect_april_tag(self,tag_id=None):
        ret, frame = self.video.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = self.april_detector.detect(img)
        if result: 
            #print ("Tag Found: ")
            for r in result:
                #print ("  ", r.tag_id)
                pass
            if tag_id == None:
                return int(img.shape[0]/2-result[0].center[1])
            else:
                for r in result:
                    if tag_id == 'yellow':
                        tag_list = (1,2,3,4,5,6)
                    else:
                        tag_list = (7,8,9,10,11,12)
                    if r.tag_id in tag_list:
                        self.state.april_detected = True
                        err = (int(img.shape[1]/2-r.center[0]), #target is centered in x but top of screen in y
                               int((img.shape[0]-20)-r.center[1]))
                        self.obj_err = (err[0]/640,err[1]/480)
                        break
                    else:
                        self.state.april_detect = False
        else:
            self.state.april_detected = False
            return 0
        #output alters state


    def detect_target_in_range(self):
        if self._get_distance() < 60: #target in range when within 60cm (2ft)
            self.state.target_inrange = True 
        else:
            self.state.target_inrange = False


    def detect_target_captured(self):
        if self._get_distance() < 15:
            #self.state.target_captured = True ---uncomment this
            self.state.target_captured = False
        else:
            self.state.target_captured = False


    def perform_search_for_object(self,obj_type):
        '''Perform search pattern for objects, counter-clockwise helical pattern
        Pattern repeats based on self.pattern_time'''
        srch_fwd_len = 3.0
        srch_coast_len = 5.0
        srch_yaw_len = 0.1
        thrust_pwr = -1.0
        yaw_pwr = -0.3
        if yaw_pwr < 0:
            yaw_correct = -1*(yaw_pwr-0.0)
        else:
            yaw_correct = -1*(yaw_pwr+0.0)

        
        if self._get_distance() > 250: #LIDAR is at 39deg angle
            self.alt_err = self.detect_april_tag() #using april tag for altitude adjustment
            if self.alt_err >= 0: #if no april tag found or april tag is above blimp perform climb else don't mess with altitude 
                self.action.climb = 1.0
                self.action.descend = 0.0
                self.alt_correct = True
            else:
                self.action.climb = 0.0
                self.action.descend = 0.0
                self.alt_correct = False
        else: 
            self.action.climb = 0.0
            self.action.descend = 0.0
            self.alt_correct = False

        if self.srch_prev_act == None:
            self.search_timer = time()
            self.action.thrust = thrust_pwr
            self.action.yaw = 0.0
            self.srch_prev_act = 'fwd'

        elif self.srch_prev_act == 'fwd':
            if time() - self.search_timer > srch_fwd_len:
                self.action.thrust = 0.0
                self.action.yaw = yaw_pwr
                self.search_timer = time()
                self.srch_prev_act = 'yaw'
            else:
                self.action.thrust = thrust_pwr
               
        elif self.srch_prev_act == 'yaw':
            if time() - self.search_timer > srch_yaw_len:
                self.action.thrust = 0.0
                self.action.yaw = 0.0
                self.search_timer = time()
                self.srch_prev_act = 'cst'
                self.yaw_correction_tmr = time()
                self.yaw_correction = True
                self.action.yaw = -1*(yaw_pwr-0.1)
            else:
                self.action.yaw = yaw_pwr

        elif self.srch_prev_act == 'cst':
            if time() - self.search_timer > srch_coast_len:
                self.action.thrust = thrust_pwr
                self.action.yaw = 0.0
                self.search_timer = time()
                self.srch_prev_act = 'fwd'
            else:
                self.action.thrust = 0.0
                if self.yaw_correction == True:
                    if time() - self.yaw_correction_tmr > (srch_yaw_len+1.0):
                        self.action.yaw = 0
                        self.yaw_correction = False
   

    def perform_move_to_object(self,object):
        '''uses self.obj_err and PID control to guide blimpy towards object'''
        #max measured yaw rate is 3sec/180deg #TODO measure this with new turning motors
        #max yaw rate should never be above +/-3 NOTE normalize yaw rate to one
        max_yaw_rate = 3.0

        #try:
        #    old_yaw = self._get_yaw()
        #    if old_yaw != None:
        #        sleep(0.05)
        #        current_yaw = self._get_yaw()
        #        yaw_rate = current_yaw - old_yaw
        #    else:
        #        yaw_rate = 0.0

        #    if abs(yaw_rate) > 180:
        #        yaw_rate = 360%abs(yaw_rate)
        #except: 
        #    pass
        
        resultx = self.pidx(self.obj_err[0])
        resulty = self.obj_err[1] #no pid just go up full throttle

        #It only climbs never sends descend commands since it descends on its own
        if resulty > 0.0:
            self.action.climb = 1.0
        else:
            self.action.climb = 0.5 #maintain lift #TODO Adjust to value that maintains lift
            #self.action.climb = abs(resulty)
        #else:
        #   self.action.descend = resulty

        if resultx < 0.1 and resultx > 0.0:
            resultx = 0.11
        elif resultx > -0.1 and resultx < 0.0:
            resultx = -0.11

        if resultx < 0.0:
            resultx = resultx*0.9

        self.action.yaw=resultx

        #print("PID Yaw: ", resultx, "PID Climb:", resulty, "Error: ", self.obj_err)
      
                #if len(self.lidar_list) >= 50:
                #    self.lidar_list.pop(0)
                #self.lidar_list.append(dist)

        #if len(self.lidar_list) == 50:
         #   obj_range = []
        #    for l in self.lidar_list:
        #        if l < 500:
        #            obj_range.append(l)
        #    if len(obj_range) >= 10:
        #        actual_range = sum(obj_range)/len(obj_range)

         #   try:
        #        print ("Distance to Target: ", actual_range)
        #    except:
        #        print("No target range.")

        #if resultx < 0.1 and resultx > 0:
        #    self.action.yaw = -1.0
        #else:
        #    self.action.yaw = 1.0

        #perform yaw maneuver adjusts for current yaw rate
        #if (yaw_rate < 0 and resultx < 0) or (yaw_rate < 0 and resultx > 0):
         #   action_time = abs(resultx)-abs(yaw_rate/max_yaw_rate)
        #elif (yaw_rate > 0 and resultx < 0) or (yaw_rate < 0 and resultx > 0):
         #   action_time = abs(yaw_rate/max_yaw_rate) + abs(resultx)
        #self.perform_action()
        #sleep(action_time)

        #counter maneuver before next loop
        #if resultx < 0:
         #   self.action.yaw = 1.0
        #else:
        #    self.action.yaw = -1.0
        #self.perform_action()
        #sleep(0.1) #TODO adjust this time to counter yaw movements

        #self.action.yaw = 0
        #self.perform_action()

        self.action.thrust = -0.11
        #self.action.thrust = -0.5 #TODO adjust to maintain forward monmentum, but not too much


    def perform_orient_to_goal(self):
        #use results of detect_april_tag to move towards goal
        pass
        #output is self.action


    def perform_target_capture(self):
        '''Once target is in range perform fine movements to ensure ball is captured'''
        self.action.yaw = 0
        self.action.thrust = 0.5


    def observe_orient_decide(self):
        '''Makes observations, determines current state, decides the appropriate action based
        on current state'''
        #self.previous_action = self.action
        #self.read_joystick_event()
        start = time()
        if self.state.in_position == True:
            self.detect_goal_scored()
            if self.state.goal_achieved == True:
                    for atr in self.state:   #Game Over we win return to ready state
                        self.state[atr] = False
            else:
                #self.detect_target_captured()
                if self.state.target_captured == True:
                    #self.detect_object('goal')
                    if self.g_color == 'orange':
                        self.detect_april_tag('orange')
                    else:
                        self.detect_april_tag('yellow')

                    if self.state.april_detected == True:
                        self.perform_move_to_object('goal')
                    else:
                        self.perform_search_for_object('goal')
                else:
                    self.detect_object('target')
                    if self.state.target_located == True:

                        #self.detect_target_in_range() #NOTE removed this because we are doing it manually
                        if self.state.target_inrange == True:
                            self.perform_target_capture()
                        else:
                            self.perform_move_to_object('target')
                    else:
                        self.perform_search_for_object('target')
                        
        

if __name__ == '__main__':
    if len(sys.argv) == 2:
        g_color = sys.argv[1]
    else:
        print("Missing Goal Color!")
        sys.exit()
    blimpy = Blimpy(g_color, pic_server=True)
    dt = time()
    while not blimpy.exiting:

        try:
            start = time()
            blimpy.observe_orient_decide()

            for state in STATE: #Print current state to screen
                if tuple(blimpy.state.values()) == STATE[state]:
                    if time() - dt > 1.0:
                        dist = blimpy._get_distance()
                        print("Distance to Ceiling: ", dist)
                        print("State: ", state)
                        dt = time()

            blimpy.perform_action() #sends motor commands 
            #print("Control Loop Time: ", time()-start)
        except KeyboardInterrupt:
            blimpy.exiting = True
            print("Blimpy Exiting!!")

