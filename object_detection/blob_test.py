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
image = np.zeros((480,640),dtype='uint8')
target_mask = np.array([[30,100,50],[60,255,255]])
while not shudder:
    shudder = read_shudder()
ret, frame = video.read() #capture image
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask_weight = np.sum(np.sum((hsv > 0).astype(int))) 
print("This much Green: ", mask_weight)
#ret, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
#thresh = cv2.convertScaleAbs(im)
#print(type(image))

#gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(image, 225, 255, cv2.THRESH_BINARY_INV)

params = cv2.SimpleBlobDetector_Params()
params.filterByArea= True
params.minArea = 100
params.filterByCircularity = True
params.minCircularity = 0.1
params.maxCircularity = 0.6
#params.minThreshold = 200;
#params.maxThreshold = 255;
params.filterByColor = False
#params.blobColor = 0
params.filterByInertia = True
params.filterByConvexity = False
#print("BLOB COLOR: ", params.blobColor)
#print (params.filterByColor)
#print (params.filterByArea)
#print (params.filterByCircularity)
#print (params.filterByInertia)
#print ("Inertia: ", params.minInertiaRatio, params.maxInertiaRatio)
#print (params.filterByConvexity)
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(image)

im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
for keypoint in keypoints:
    print("SIZE: ", keypoint.size)
    cv2.circle(im_with_keypoints, (int(keypoint.pt[0]),int(keypoint.pt[1])), 5,(255,0,0),-1)
   #print("X: ", keypoint.x)
    #print("Y: ", keypoint.y)


#contours, hierarchy = cv2.findContours(image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

#image_copy = image.copy()

#cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)



#cv2.imshow("Color Detected", im_with_keypoints)
cv2.imwrite("blob_detected.jpg", im_with_keypoints)
cv2.imwrite("contours.jpg", image_copy)
#cv2.imshow("Color Detected", np.hstack((image,output)))
#cv2.waitKey(0)
#cv2.destroyAllWindows()
