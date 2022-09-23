import cv2
from time import sleep
import numpy as np
import time
import statistics as stat
import pickle
from simple_pid import PID
import imutils
from imutils import perspective
from imutils import contours

#video = cv2.VideoCapture(0)
#ret, frame = video.read() #capture image
#max_len_images = 10
#for i in range(max_len_images):
#    ret, frame = video.read()
#    if ret == True:
#        if i == 0:
#            avg_image = frame
#        else:
#            a = 1.0/(i+1)
#            b = 1 - a
#            avg_image = cv2.addWeighted(frame,a,avg_image,b,0.0) #average image
#hsv = cv2.cvtColor(avg_image,cv2.COLOR_BGR2HSV) #convert to HSV

frame = cv2.imread("/Users/adambarker/Documents/Personal Stuff/School/PhD/Research/Robotics/LTA/dtr_open/Blimp/object_detection_openCV/test_images/captured_030322/image_1644609228.3756137.jpg")  
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
target_mask = np.array([[30,0,50],[60,255,255]])
mask = cv2.inRange(frame,target_mask[0],target_mask[1])
#ret, thresh = cv2.threshold(im, 150, 255, cv2.THRESH_BINARY)
#thresh = cv2.convertScaleAbs(im)
#print(type(image))
#gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#_, binary = cv2.threshold(mask, 225, 255, cv2.THRESH_BINARY_INV)
#_, binary = cv2.threshold(image,225,255, cv2.THRESH_BINARY_INV)
#thresh_inverse = cv2.bitwise_not(binary)
#cv2.imshow("Not", thresh_inverse)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#print("Image: ", image.dtype, image.shape, "Gray: ", image.dtype, image.shape, "Inverse: ", thresh_inverse.dtype, thresh_inverse.shape)
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_blob = max(contours, key=lambda el: cv2.contourArea(el))

print("AREA: ", cv2.contourArea(largest_blob))
image_copy = frame.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
cv2.drawContours(image=image_copy, contours=largest_blob, contourIdx=-1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
M = cv2.moments(largest_blob)
center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#print("CENTER ", center)
goal = (int(image_copy.shape[1]/2), int(image_copy.shape[0]/20))

cv2.circle(image_copy, goal, 10, (100,255,100), -1)
#canvas = mask.copy()
cv2.circle(image_copy, center, 10, (255,0,0), -1)
cv2.imshow("Color Detected", image_copy)
#cv2.imshow("Color Detected", np.hstack((image,output)))
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite("contour_test_{}.jpg".format(time.time()),image_copy)
