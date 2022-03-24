import cv2
from time import sleep
import numpy as np
import time
import statistics as stat
import pickle

#CONVERT TO HSV
#hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#hsv_mask_lower = np.array([Hue,Sat,Value])
#hsv_mask_upper = np.array([Hue,Sat,Value])
cap_time = []
tot_time = []
upper = [99,77,99]
lower = [18,49,52]
lower = np.array(lower,dtype='uint8')
upper = np.array(upper, dtype='uint8')
vid = cv2.VideoCapture(0)
ret, frame = vid.read()
mask = cv2.inRange(frame, lower, upper)
gX = int(mask.shape[1]/2) #goal X
gY = int(mask.shape[0]/2) #goal Y
M = cv2.moments(mask)
try:
     cX = int(M["m10"] / M["m00"]) #centroid X
     cY = int(M["m01"] / M["m00"]) #centroid Y
     #output = cv2.bitwise_and(frame, frame, mask = mask)
     errX = gX - cX
     errY = gY - cY
except ZeroDivisionError:
    print ("No Moment") 
output = cv2.bitwise_and(frame,frame, mask = mask)
cv2.imshow('images',mask)
print(np.sum(np.sum(mask)))
cv2.waitKey(0)
#cv2.imwrite("color_detect.jpg", np.hstack([frame,output]))
