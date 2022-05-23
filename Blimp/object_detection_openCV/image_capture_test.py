import cv2
import evdev
from evdev import InputDevice, categorize, ecodes
from time import sleep
import numpy as np
import time
import statistics as stat
import pickle
from simple_pid import PID
import imutils
#from imutils import perspective
#from imutils import contours

joystick = None
while not joystick:
            devices = [InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                if device.name[0:15] == 'PLAYSTATION(R)3':
                    joystick = device
                    break
            print ("Waiting on controller connection.")
            sleep(1)
print("Controller Connected.")

def read_shudder(joy_max=127):
        '''Read a single evdev event from joystick.
        joy_max is max value for EV_ABS events'''

        if not joystick: #no joystick connected
            return False

        event = joystick.read_one()
        if event != None:
            if event.type == ecodes.EV_KEY:
                try:
                    if ecodes.keys[event.code] == 'BTN_DEAD':
                        if event.value == 1:
                            return True
                        else:
                            return False
                except KeyError: #Non-mapped button pressed
                    pass
shudder = False
video = cv2.VideoCapture(0)
#image = np.zeros((480,640),dtype='uint8')
#target_mask = np.array([[30,100,50],[60,255,255]])
time.sleep(5)
while True:
    shudder = read_shudder()
    if shudder:
        ret, frame = video.read() #capture image
        if ret:
            cv2.imwrite("image_{}.jpg".format(time.time()),frame)
            print("Image Captured")

#cv2.imshow("Color Detected", np.hstack((image,output)))
#cv2.waitKey(0)
#cv2.destroyAllWindows()
