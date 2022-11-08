
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
import  math

<<<<<<< HEAD
thresholds = [(54, 100, -39, -7, 29, 85), #yellow 0
              (6, 60, -103, -9, -64, 100), #green 1
              (34, 43, 11, 48, 21, 55)] #orange 2
=======
# ledRed = pyb.LED(1) # Initiates the red led
# ledGreen = pyb.LED(2) # Initiates the green led
# ledBlue = pyb.LED(3) # Initiates the blue led
# ledIR = pyb.LED(4) # Initiates the IR led


thresholds = [(64, 100, -36, -11, 8, 127), #yellow 0
              (0, 70, -59, -12, -10, 54), #green 1
              (35, 62, 29, 93, 35, 98)] #orange 2
>>>>>>> autonomousFlight1



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
orange_goalx_ema = None
orange_goaly_ema = None
yellow_goalx_ema = None
yellow_goaly_ema = None
SQerror = 0

# data on selected ball (all three are instances of EMA)
x_ema = None
y_ema = None
rect_ema = None #This is bounding box of ball, used to determine what is the closest

#misc. variables
alpha_rect = .85 # alpha value of the rectangle that bounds the ball
goal_alpha = .85 # alpha value of the rectangle that bounds the goal
ball_alpha = .85 # alpha value of the centroid of the ball

orange_goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
orange_goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)
yellow_goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
yellow_goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)


ball_xerror = 0 # Distance in pixels away from the ball horizontally (int)
ball_yerror = 0 # Distance in pixels away from the ball vertically (int)

dist_ball = 0 # (float)
dist_goal = 0 # (float)

def find_ball(img):
    blobs = img.find_blobs([thresholds[1]], pixels_threshold=50, area_threshold=20, merge=True,  margin = 10)
    biggest = [(sensor.width()/2),(sensor.height()/2),0,0] #[x, y, width, height]
    r = [0,0,0,0]
    global x_ema
    global y_ema
    global ball_xerror
    global ball_yerror
    global rect_ema
    global alpha_rect
    global dist_ball
    dataClasses.data.ballIsFound = 0
    for blob in blobs:
        dataClasses.data.ballIsFound = 1
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        if current[2] > biggest[2]:
            biggest = current
            r = blob.rect()
    if x_ema == None:
        x_ema = EMA(biggest[0], ball_alpha)
<<<<<<< HEAD
        rect_ema = [EMA(r[0], alpha_rect),
        EMA(r[1], alpha_rect),
        EMA(r[2], alpha_rect),
        EMA(r[3], alpha_rect)]
=======
        rect_ema = [EMA(r[0], alpha_rect), EMA(r[1], alpha_rect), EMA(r[2], alpha_rect), EMA(r[3], alpha_rect)]
>>>>>>> autonomousFlight1
        y_ema = EMA(biggest[1], ball_alpha)
    else:
        x_ema.update(biggest[0])
        y_ema.update(biggest[1])
        rect_ema[0].update(r[0])
        rect_ema[1].update(r[1])
        rect_ema[2].update(r[2])
        rect_ema[3].update(r[3])
<<<<<<< HEAD
    #if (rect_ema[2].get_value() != 0):
        #dist_ball = 22/(math.tan((rect_ema[2].get_value() * .22125)/2)) #rect_ema[2].getvalue() gives ball width, use equation for pixel width to meters away
    #img.draw_rectangle(blob.rect())
    if dataClasses.data.ballIsFound == 1:
        img.draw_rectangle([round(ema.get_value()) for ema in rect_ema], [0, 255, 0])
        img.draw_string(round(rect_ema[0].get_value()),round(rect_ema[1].get_value()), " Ball", [0, 255, 0], mono_space = False)
        #img.draw_cross(blob.cx(), blob.cy())
        img.draw_cross(round(x_ema.get_value()), round(y_ema.get_value()), [0, 255, 0])
=======
    if (rect_ema[2].get_value() != 0):
        dist_ball = 22/(math.tan((rect_ema[2].get_value() * .22125)/2)) #rect_ema[2].getvalue() gives ball width, use equation for pixel width to meters away
    #img.draw_rectangle(blob.rect())
    img.draw_rectangle([round(ema.get_value()) for ema in rect_ema], 2)
    img.draw_string(round(rect_ema[0].get_value()),round(rect_ema[1].get_value()), " Ball", [0, 0, 255], mono_space = False)
    #img.draw_cross(blob.cx(), blob.cy())
    img.draw_cross(round(x_ema.get_value()), round(y_ema.get_value()), 2)
>>>>>>> autonomousFlight1
    dataClasses.data.ball_xerror = round(x_ema.get_value()) - (sensor.width()/2)
    dataClasses.data.ball_yerror = round(y_ema.get_value()) - (sensor.height()/2)
   # dataClasses.data.ballIsFound = len(blob)
    return

def find_yellow_goal(img):
    blobs = img.find_blobs([thresholds[0]], pixels_threshold=4, area_threshold=7, merge=True, margin=10)
    biggest = [int((sensor.width()/2)),int((sensor.height()/2)),0,0] #[cx, cy, width, height]
    r = [0,0,0,0]
    counter = 0
    global dist_goal
    global yellow_goalx_ema
    global yellow_goaly_ema
    global SQerror
<<<<<<< HEAD
    global yellow_goal_xerror
    global yellow_goal_yerror
=======
    global goal_xerror
    global goal_yerror
>>>>>>> autonomousFlight1
    dataClasses.data.yellowGoalIsFound = 0
    for blob in blobs:
        dataClasses.data.yellowGoalIsFound = 1
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        #img.draw_rectangle(blob.rect())
        #img.draw_cross(current[0], current[1])
        counter = counter + 1
        width = current[2]
        height = current[3]
        SQerror = width/height
        if current[3] > biggest[3]:
            biggest = current
    if yellow_goalx_ema == None:
        yellow_goalx_ema = EMA(biggest[0], goal_alpha)
        yellow_goaly_ema = EMA(biggest[1], goal_alpha)
    else:
        yellow_goalx_ema.update(biggest[0])
        yellow_goaly_ema.update(biggest[1])
    if (biggest[3] != 0):
        dist_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal

    if dataClasses.data.yellowGoalIsFound == 1:
        img.draw_cross(round(yellow_goalx_ema.get_value()), round(yellow_goaly_ema.get_value()), color=[255, 255, 0])
        img.draw_string(biggest[0], biggest[1],"Selected Yellow Goal",[255, 255, 0] , mono_space = False)
        #img.draw_cross(biggest[0], biggest[1])
    dataClasses.data.goal_yellow_xerror = round(yellow_goalx_ema.get_value()) - (sensor.width()/2)
    dataClasses.data.goal_yellow_goal_yerror = round(yellow_goaly_ema.get_value()) - (sensor.height()/2)
    return

def find_orange_goal(img):
    blobs = img.find_blobs([thresholds[2]], pixels_threshold=9, area_threshold=25, merge=True, margin=10)
    biggest = [int((sensor.width()/2)),int((sensor.height()/2)),0,0] #[cx, cy, width, height]
    r = [0,0,0,0]
    counter = 0
    global dist_goal
    global orange_goalx_ema
    global orange_goaly_ema
    global SQerror

    global orange_goal_xerror
    global orange_goal_yerror

    dataClasses.data.orangeGoalIsFound = 0
    for blob in blobs:
        dataClasses.data.orangeGoalIsFound = 1
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        #img.draw_rectangle(blob.rect())
        #img.draw_cross(current[0], current[1])
        counter = counter + 1
        width = current[2]
        height = current[3]
        SQerror = width/height
        if current[3] > biggest[3]:
            biggest = current
    if orange_goalx_ema == None:
        orange_goalx_ema = EMA(biggest[0], goal_alpha)
        orange_goaly_ema = EMA(biggest[1], goal_alpha)
    else:
        orange_goalx_ema.update(biggest[0])
        orange_goaly_ema.update(biggest[1])
    if (biggest[3] != 0):
        dist_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal

    if dataClasses.data.orangeGoalIsFound == 1:
        img.draw_string(biggest[0], biggest[1],"Selected Orange Goal",[255, 127, 0] , mono_space = False)
        #img.draw_cross(biggest[0], biggest[1])
        img.draw_cross(round(orange_goalx_ema.get_value()), round(orange_goaly_ema.get_value()), color=[255, 127, 0])
    dataClasses.data.goal_orange_xerror = round(orange_goalx_ema.get_value()) -(sensor.width()/2)
    dataClasses.data.goal_orange_goal_yerror = round(orange_goaly_ema.get_value()) - (sensor.height()/2)
    return






























# class TagInfo:
#     def __init__(self):
#         self.foundIt = 0
#         self.tags = None
#         self.rotation = None

<<<<<<< HEAD
tagsFound = TagInfo()

=======
# tagsFound = TagInfo()
    
>>>>>>> autonomousFlight1

# def lookForAprilTag(img):
#     logger.log.verbose("in look for april tag")

<<<<<<< HEAD
    foundIt = 0

    for tag in img.find_apriltags(): # defaults to TAG36H11 without "families".
        tagsFound.foundIt = 1
        tagsFound.tags = tag
        tagsFound.rotation = (180 * tag.rotation()) / math.pi
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        logger.log.verbose("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)
=======
#     foundIt = 0
    
#     for tag in img.find_apriltags(): # defaults to TAG36H11 without "families".        
#         tagsFound.foundIt = 1 
#         tagsFound.tags = tag 
#         tagsFound.rotation = (180 * tag.rotation()) / math.pi    
#         print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
#         logger.log.verbose("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)
>>>>>>> autonomousFlight1

#     logger.log.verbose("found april tag?: " + str(tagsFound.foundIt))

#     return tagsFound

<<<<<<< HEAD
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

=======
# def family_name(tag):
#     if(tag.family() == image.TAG16H5):
#         return "TAG16H5"
#     if(tag.family() == image.TAG25H7):
#         return "TAG25H7"
#     if(tag.family() == image.TAG25H9):
#         return "TAG25H9"
#     if(tag.family() == image.TAG36H10):
#         return "TAG36H10"
#     if(tag.family() == image.TAG36H11):
#         return "TAG36H11"
#     if(tag.family() == image.ARTOOLKIT):
#         return "ARTOOLKIT"  
>>>>>>> autonomousFlight1
