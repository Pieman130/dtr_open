
from dataClasses import ProcessedData
import dataClasses
import logger

if dataClasses.config.isMicroPython:
    import image # for stupid example

import time
import math
class EMA:
    def __init__(self, value, alpha = 0.5):
        self.value = value
        self.alpha = alpha
        self.alpha_compl = 1 - alpha
    def update(self, value):
        self.value = self.alpha * self.value + self.alpha_compl * value
    def get_value(self):
        return self.value

#Copied from OpenMV_ide_prototype.py, edited to better fit code structure
import sensor, image, time, math, ustruct, sys, pyb, pid
from pyb import USB_VCP, Pin, Timer, Servo

ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led
ledBlue = pyb.LED(3) # Initiates the blue led
ledIR = pyb.LED(4) # Initiates the IR led


thresholds = [(64, 100, -36, -11, 8, 127), #yellow 0
              (0, 70, -59, -12, -10, 54), #green 1
              (35, 62, 29, 93, 35, 98)] #orange 2



#These are the sensor parameters for color detection to work optimally:
"""
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 200)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(True) # must be turned off for color tracking (I ignored this and kept it on)
clock = time.clock()
"""
# data on selected goal (goalx and goaly are instances of EMA)
goalx_ema = None
goaly_ema = None
SQerror = 0

# data on selected ball (all three are instances of EMA)
x_ema = None
y_ema = None
rect_ema = None #This is bounding box of ball, used to determine what is the closest

#misc. variables
alpha_rect = .85 # alpha value of the rectangle that bounds the ball
goal_alpha = .85 # alpha value of the rectangle that bounds the goal
ball_alpha = .85 # alpha value of the centroid of the ball

goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)

ball_xerror = 0 # Distance in pixels away from the ball horizontally (int)
ball_yerror = 0 # Distance in pixels away from the ball vertically (int)

dist_ball = 0 # (float)
dist_goal = 0 # (float)

def find_ball(img):
    blobs = img.find_blobs([thresholds[1]], pixels_threshold=50, area_threshold=50, merge=True,  margin = 10)
    biggest = [0,0,0,0] #[x, y, width, height]
    global x_ema
    global y_ema
    global ball_xerror
    global ball_yerror
    global rect_ema
    global alpha_rect
    global dist_ball
    for blob in blobs:
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        if current[2] > biggest[2]:
            biggest = current
            r = blob.rect()
    if x_ema == None:
        x_ema = EMA(biggest[0], ball_alpha)
        rect_ema = [EMA(r[0], alpha_rect), EMA(r[1], alpha_rect), EMA(r[2], alpha_rect), EMA(r[3], alpha_rect)]
        y_ema = EMA(biggest[1], ball_alpha)
    else:
        x_ema.update(biggest[0])
        y_ema.update(biggest[1])
        rect_ema[0].update(r[0])
        rect_ema[1].update(r[1])
        rect_ema[2].update(r[2])
        rect_ema[3].update(r[3])
    if (rect_ema[2].get_value() != 0):
        dist_ball = 22/(math.tan((rect_ema[2].get_value() * .22125)/2)) #rect_ema[2].getvalue() gives ball width, use equation for pixel width to meters away
    #img.draw_rectangle(blob.rect())
    img.draw_rectangle([round(ema.get_value()) for ema in rect_ema], 2)
    img.draw_string(round(rect_ema[0].get_value()),round(rect_ema[1].get_value()), " Ball", [0, 0, 255], mono_space = False)
    #img.draw_cross(blob.cx(), blob.cy())
    img.draw_cross(round(x_ema.get_value()), round(y_ema.get_value()), 2)
    dataClasses.data.ball_xerror = round(x_ema.get_value()) - 160
    dataClasses.data.ball_yerror = round(y_ema.get_value()) - 120
   # dataClasses.data.ballIsFound = len(blob)
    return

def find_yellow_goal(img):
    blobs = img.find_blobs([thresholds[0]], pixels_threshold=3, area_threshold=12, merge=True, margin=10)
    biggest = [160,120,0,0] #[cx, cy, width, height]
    counter = 0
    global dist_goal
    global goalx_ema
    global goaly_ema
    global SQerror
    global goal_xerror
    global goal_yerror
    for blob in blobs:
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        img.draw_rectangle(blob.rect())
        #img.draw_cross(current[0], current[1])
        counter = counter + 1
        width = current[2]
        height = current[3]
        SQerror = width/height
        if current[3] > biggest[3]:
            biggest = current
    img.draw_string(biggest[0], biggest[1],"Selected Yellow Goal",[0, 0, 255] , mono_space = False)
    img.draw_cross(biggest[0], biggest[1])
    if goalx_ema == None:
        goalx_ema = EMA(biggest[0], goal_alpha)
        goaly_ema = EMA(biggest[1], goal_alpha)
    else:
        goalx_ema.update(biggest[0])
        goaly_ema.update(biggest[1])
    if (biggest[3] != 0):
        dist_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
    img.draw_cross(round(goalx_ema.get_value()), round(goaly_ema.get_value()), color=[0,0,0])
    dataClasses.data.goal_yellow_xerror = 160 - round(goalx_ema.get_value())
    dataClasses.data.goal_yellow_goal_yerror = round(goaly_ema.get_value()) - 120
    return
def find_orange_goal(img):
    blobs = img.find_blobs([thresholds[2]], pixels_threshold=3, area_threshold=12, merge=True, margin=10)
    biggest = [160,120,0,0] #[cx, cy, width, height]
    counter = 0
    global dist_goal
    global goalx_ema
    global goaly_ema
    global SQerror
    global goal_xerror
    global goal_yerror
    for blob in blobs:
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        img.draw_rectangle(blob.rect())
        #img.draw_cross(current[0], current[1])
        counter = counter + 1
        width = current[2]
        height = current[3]
        SQerror = width/height
        if current[3] > biggest[3]:
            biggest = current
    img.draw_string(biggest[0], biggest[1],"Selected Orange Goal",[0, 0, 255] , mono_space = False)
    img.draw_cross(biggest[0], biggest[1])
    if goalx_ema == None:
        goalx_ema = EMA(biggest[0], goal_alpha)
        goaly_ema = EMA(biggest[1], goal_alpha)
    else:
        goalx_ema.update(biggest[0])
        goaly_ema.update(biggest[1])
    if (biggest[3] != 0):
        dist_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
    img.draw_cross(round(goalx_ema.get_value()), round(goaly_ema.get_value()), color=[0,0,0])
    dataClasses.data.goal_orange_xerror = 160 - round(goalx_ema.get_value())
    dataClasses.data.goal_orange_goal_yerror = round(goaly_ema.get_value()) - 120
    return






























class TagInfo:
    def __init__(self):
        self.foundIt = 0
        self.tags = None
        self.rotation = None

tagsFound = TagInfo()
    

def lookForAprilTag(img):
    logger.log.verbose("in look for april tag")

    foundIt = 0
    
    for tag in img.find_apriltags(): # defaults to TAG36H11 without "families".        
        tagsFound.foundIt = 1 
        tagsFound.tags = tag 
        tagsFound.rotation = (180 * tag.rotation()) / math.pi    
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        logger.log.verbose("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)

    logger.log.verbose("found april tag?: " + str(tagsFound.foundIt))

    return tagsFound

def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"  
