import pickle
import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics as stat

mask = pickle.load(open("/Users/adambarker/Desktop/PhD/Research/Robotics/LTA/mask_img.p", "rb"))
image = cv2.imread("/Users/adambarker/Desktop/PhD/Research/Robotics/LTA/dryerase.jpg")
mX = int(mask.shape[1]/2) #goal X
mY = int(mask.shape[0]/2) #goal Y
M = cv2.moments(mask)
cX = int(M["m10"] / M["m00"]) #centroid X
cY = int(M["m01"] / M["m00"]) #centroid Y
# put text and highlight the center
cv2.circle(image, (cX, cY), 5, (0, 255, 0), -1)
cv2.putText(image, "Centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
cv2.circle(image, (mX,mY), 5,(255,0,0),-1)
cv2.putText(image, "Goal", (mX-25,mY-25),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
cv2.arrowedLine(image, (mX,mY),(cX,cY),(0,0,255),2)
cv2.arrowedLine(image, (cX,cY),(mX,mY),(0,0,255),2)
lX = int((cX-mX)/2+mX)
lY = int((cY-mY)/2+mY)
cv2.putText(image, "Error", (lX-25,lY-5),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
# display the image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.imwrite("relative_error.jpg", image)
