import cv2
from time import sleep
import numpy as np
import time
#import statistics as stat
#import pickle
#from simple_pid import PID
#import imutils
#from imutils import perspective
#from imutils import contours

video = cv2.VideoCapture(0)
ret, frame = video.read() #capture image
#image = cv2.imread("/Users/adambarker/Desktop/PhD/Research/Robotics/LTA/laptop_mask.jpg")  
print("RET" , ret)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

target_mask = np.array([[50,100,130],[70,255,255]])
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
#largest_blob = max(contours, key=lambda el: cv2.contourArea(el))
image_copy = frame.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
#cv2.drawContours(image=image_copy, contours=largest_blob, contourIdx=-1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
#M = cv2.moments(largest_blob)
#center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
canvas = mask.copy()
#cv2.circle(canvas, center, 2, (0,0,255), -1)
cv2.imshow("Color Detected", image_copy)
#cv2.imshow("Color Detected", np.hstack((image,output)))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("contour_test_{}.jpg".format(time.time()),image_copy)
