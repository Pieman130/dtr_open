
from dataClasses import ProcessedData
import dataClasses
import logger
import  math
import time

if dataClasses.config.isMicroPython:
    import image # for stupid example

class EMA:
    def __init__(self, value, alpha = 0.5):
        self.value = value
        self.alpha = alpha
        self.alpha_compl = 1 - alpha
    def update(self, value):
        self.value = self.alpha * self.value + self.alpha_compl * value
    def get_value(self):
        return self.value

<<<<<<< HEAD
<<<<<<< Updated upstream
#Copied from OpenMV_ide_prototype.py, edited to better fit code structure
=======
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081

THRESHOLDS = [(64, 100, -36, -11, 8, 127), #yellow 0
              (0, 70, -59, -12, -10, 54), #green 1
<<<<<<< HEAD
              (17, 100, 14, 70, 34, 127)] #orange 2


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
                x_ema = EMA(current[0], ball_alpha)
                rect_ema = [EMA(r[0], alpha_rect), EMA(r[1], alpha_rect), EMA(r[2], alpha_rect), EMA(r[3], alpha_rect)]
                y_ema = EMA(current[1], ball_alpha)
            else:
                x_ema.update(current[0])
                y_ema.update(current[1])
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










=======
>>>>>>> Stashed changes

THRESHOLDS = [(64, 100, -36, -11, 8, 127), #yellow 0
              (0, 70, -59, -12, -10, 54), #green 1
=======
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
              (35, 62, 29, 93, 35, 98)] #orange 2

class ImageProcessing():
    def __init__(self):
<<<<<<< HEAD
<<<<<<< Updated upstream
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

#def family_name(tag):
 #   if(tag.family() == image.TAG16H5):
  #      return "TAG16H5"
  #  if(tag.family() == image.TAG25H7):
  #      return "TAG25H7"
  #  if(tag.family() == image.TAG25H9):
  #      return "TAG25H9"
  #  if(tag.family() == image.TAG36H10):
  #      return "TAG36H10"
  #  if(tag.family() == image.TAG36H11):
  #      return "TAG36H11"
   # if(tag.family() == image.ARTOOLKIT):
   #     return "ARTOOLKIT"  
=======
        #data on selected goals
        self.orange_goalx_ema = None
        self.orange_goaly_ema = None
        self.yellow_goalx_ema = None
        self.yellow_goaly_ema = None
        self.orange_SQerror = 0
        self.yellow_SQerror = 0
=======
        self.goalx_ema = None
        self.goaly_ema = None
        self.SQerror = 0
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081

        # data on selected ball (all three are instances of EMA)
        self.x_ema = None
        self.y_ema = None
        self.rect_ema = None #This is bounding box of ball, used to determine what is the closest

        #misc. variables
        self.alpha_rect = .85 # alpha value of the rectangle that bounds the ball
        self.goal_alpha = .85 # alpha value of the rectangle that bounds the goal
        self.ball_alpha = .85 # alpha value of the centroid of the ball

<<<<<<< HEAD
        self.orange_goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
        self.orange_goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)
        self.yellow_goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
        self.yellow_goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)
=======
        self.goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
        self.goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081

        self.ball_xerror = 0 # Distance in pixels away from the ball horizontally (int)
        self.ball_yerror = 0 # Distance in pixels away from the ball vertically (int)

<<<<<<< HEAD
=======
        self.dist_ball = 0 # (float)
        self.dist_goal = 0 # (float)


>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
    def find_ball(self,img):
        if img != None:
            blobs = img.find_blobs([THRESHOLDS[1]], pixels_threshold=50, area_threshold=50, merge=True,  margin = 10)
            biggest = [0,0,0,0] #[x, y, width, height]
            dataClasses.data.ballIsFound = 0
            if blobs: #something that looks like a ball was detected
                for blob in blobs:
                    dataClasses.data.ballIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
                    if current[2] > biggest[2]:
                        biggest = current
                        r = blob.rect()
                if self.x_ema == None:
                    self.x_ema = EMA(biggest[0], self.ball_alpha)
<<<<<<< HEAD
                    self.y_ema = EMA(biggest[1], self.ball_alpha)
=======
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
                    self.rect_ema = [EMA(r[0], self.alpha_rect), 
                                    EMA(r[1], self.alpha_rect), 
                                    EMA(r[2], self.alpha_rect), 
                                    EMA(r[3], self.alpha_rect)]
<<<<<<< HEAD
=======
                    self.y_ema = EMA(biggest[1], self.ball_alpha)
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
                else:
                    self.x_ema.update(biggest[0])
                    self.y_ema.update(biggest[1])
                    self.rect_ema[0].update(r[0])
                    self.rect_ema[1].update(r[1])
                    self.rect_ema[2].update(r[2])
                    self.rect_ema[3].update(r[3])
                if (self.rect_ema[2].get_value() != 0):
<<<<<<< HEAD
                    dataClasses.data.distanceToBall = 22/(math.tan((self.rect_ema[2].get_value() * .22125)/2)) #rect_ema[2].getvalue() gives ball width, use equation for pixel width to meters away
                #img.draw_rectangle(blob.rect())
                img.draw_rectangle([round(ema.get_value()) for ema in self.rect_ema], [0, 255, 0])
                img.draw_string(round(self.rect_ema[0].get_value()),round(self.rect_ema[1].get_value()), "Ball", [0, 255, 0], mono_space = False)
                #img.draw_cross(blob.cx(), blob.cy())
                img.draw_cross(round(self.x_ema.get_value()), round(self.y_ema.get_value()), [0, 255, 0])
                dataClasses.data.ball_xerror = round(self.x_ema.get_value()) - (img.width()/2)
                dataClasses.data.ball_yerror = round(self.y_ema.get_value()) - (img.height()/2)
=======
                    dist_ball = 22/(math.tan((self.rect_ema[2].get_value() * .22125)/2)) #rect_ema[2].getvalue() gives ball width, use equation for pixel width to meters away
                #img.draw_rectangle(blob.rect())
                img.draw_rectangle([round(ema.get_value()) for ema in self.rect_ema], 2)
                img.draw_string(round(self.rect_ema[0].get_value()),round(self.rect_ema[1].get_value()), " Ball", [0, 0, 255], mono_space = False)
                #img.draw_cross(blob.cx(), blob.cy())
                img.draw_cross(round(self.x_ema.get_value()), round(self.y_ema.get_value()), 2)
                dataClasses.data.ball_xerror = round(self.x_ema.get_value()) - (img.width()/2)
                dataClasses.data.ball_yerror = round(self.y_ema.get_value()) - (img.height()/2)
                print("IMAGE WIDTH: ", img.width())
                print("IMAGE HEIGHT: ", img.height())
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
         
            else: #nothing that looks like a ball was detected
                dataClasses.data.ballIsFound = 0
                dataClasses.data.ball_xerror = None
                dataClasses.data.ball_yerror = None
                logger.log.verbose("No Ball Found!")
                return
        else:
            logger.log.warning("No Image Passed to ImageProcessing!")

    def find_yellow_goal(self,img):
        if img != None:
            blobs = img.find_blobs([THRESHOLDS[0]], pixels_threshold=3, area_threshold=12, merge=True, margin=10)
            biggest = [160,120,0,0] #[cx, cy, width, height]
<<<<<<< HEAD
=======
            counter = 0
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
            #dataClasses.data.yellowGoalIsFound = 0
            if blobs: #goal like object detected
                for blob in blobs:
                    dataClasses.data.yellowGoalIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
<<<<<<< HEAD
                    width = current[2]
                    height = current[3]
                    self.yellow_SQerror = width/height
                    if current[3] > biggest[3]:
                        biggest = current
                if self.yellow_goalx_ema == None:
                    self.yellow_goalx_ema = EMA(biggest[0], self.goal_alpha)
                    self.yellow_goaly_ema = EMA(biggest[1], self.goal_alpha)
                else:
                    self.yellow_goalx_ema.update(biggest[0])
                    self.yellow_goaly_ema.update(biggest[1])
                if (biggest[3] != 0):
                    dataClasses.data.dist_yellow_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
                img.draw_cross(round(self.yellow_goalx_ema.get_value()), round(self.yellow_goaly_ema.get_value()), color=[255, 255, 0])
                img.draw_string(round(self.yellow_goalx_ema.get_value()), round(self.yellow_goaly_ema.get_value()),"Selected Yellow Goal",[255, 255, 0] , mono_space = False)
                dataClasses.data.goal_yellow_xerror = round(self.yellow_goalx_ema.get_value()) - (img.width()/2)
                dataClasses.data.goal_yellow_yerror = round(self.yellow_goaly_ema.get_value()) - (img.height()/2)
=======
                    img.draw_rectangle(blob.rect())
                    #img.draw_cross(current[0], current[1])
                    counter = counter + 1
                    width = current[2]
                    height = current[3]
                    self.SQerror = width/height
                    if current[3] > biggest[3]:
                        biggest = current
                img.draw_string(biggest[0], biggest[1],"Selected Yellow Goal",[0, 0, 255] , mono_space = False)
                img.draw_cross(biggest[0], biggest[1])
                if self.goalx_ema == None:
                    self.goalx_ema = EMA(biggest[0], self.goal_alpha)
                    self.goaly_ema = EMA(biggest[1], self.goal_alpha)
                else:
                    self.goalx_ema.update(biggest[0])
                    self.goaly_ema.update(biggest[1])
                if (biggest[3] != 0):
                    dist_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
                img.draw_cross(round(self.goalx_ema.get_value()), round(self.goaly_ema.get_value()), color=[0,0,0])
                dataClasses.data.goal_yellow_xerror = round(self.goalx_ema.get_value()) - (img.width()/2)
                dataClasses.data.goal_yellow_yerror = round(self.goaly_ema.get_value()) - (img.height()/2)
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081

            else: #nothing that looks like a goal was detected
                dataClasses.data.yellowGoalIsFound = 0
                dataClasses.data.goal_yellow_xerror = None
                dataClasses.data.goal_yellow_yerror = None
                logger.log.verbose("Yellow Goal Not Found!")
                return
        else:
            logger.log.warning("No Image Passed to ImageProcessing!")

    def find_orange_goal(self,img):
        if img != None:
            blobs = img.find_blobs([THRESHOLDS[2]], pixels_threshold=3, area_threshold=12, merge=True, margin=10)
            biggest = [160,120,0,0] #[cx, cy, width, height]
<<<<<<< HEAD
=======
            counter = 0
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
            #dataClasses.data.orangeGoalIsFound = 0
            if blobs: #goal like object detected
                for blob in blobs:
                    dataClasses.data.orangeGoalIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
<<<<<<< HEAD
=======
                    img.draw_rectangle(blob.rect())
                    #img.draw_cross(current[0], current[1])
                    counter = counter + 1
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
                    width = current[2]
                    height = current[3]
                    self.SQerror = width/height
                    if current[3] > biggest[3]:
                        biggest = current
<<<<<<< HEAD
                if self.orange_goalx_ema == None:
                    self.orange_goalx_ema = EMA(biggest[0], self.goal_alpha)
                    self.orange_goaly_ema = EMA(biggest[1], self.goal_alpha)
                else:
                    self.orange_goalx_ema.update(biggest[0])
                    self.orange_goaly_ema.update(biggest[1])
                if (biggest[3] != 0):
                    dataClasses.data.dist_orange_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
                img.draw_cross(round(self.orange_goalx_ema.get_value()), round(self.orange_goaly_ema.get_value()), color=[255, 165, 0])
                img.draw_string(round(self.orange_goalx_ema.get_value()), round(self.orange_goaly_ema.get_value()),"Selected Orange Goal",[255, 165, 0] , mono_space = False)
                dataClasses.data.goal_orange_xerror = round(self.orange_goalx_ema.get_value()) -(img.width()/2)
                dataClasses.data.goal_orange_yerror = round(self.orange_goaly_ema.get_value()) - (img.height()/2)
=======
                img.draw_string(biggest[0], biggest[1],"Selected Orange Goal",[0, 0, 255] , mono_space = False)
                img.draw_cross(biggest[0], biggest[1])
                if self.goalx_ema == None:
                    self.goalx_ema = EMA(biggest[0], self.goal_alpha)
                    self.goaly_ema = EMA(biggest[1], self.goal_alpha)
                else:
                    self.goalx_ema.update(biggest[0])
                    self.goaly_ema.update(biggest[1])
                if (biggest[3] != 0):
                    dist_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
                img.draw_cross(round(self.goalx_ema.get_value()), round(self.goaly_ema.get_value()), color=[0,0,0])
                dataClasses.data.goal_orange_xerror = round(self.goalx_ema.get_value()) -(img.width()/2)
                dataClasses.data.goal_orange_goal_yerror = round(self.goaly_ema.get_value()) - (img.height()/2)
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081

            else: #nothing that looks like a goal was detected
                dataClasses.data.orangeGoalIsFound = 0
                dataClasses.data.goal_orange_xerror = None
<<<<<<< HEAD
                dataClasses.data.goal_orange_yerror = None
=======
                dataClasses.data.goal_orange_goal_yerror = None
>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
                logger.log.verbose("Orange Goal Not Found!")
                return
        else:
            logger.log.warning("No Image Passed to ImageProcessing!")
<<<<<<< HEAD
>>>>>>> Stashed changes
=======

>>>>>>> 878a215c1d0bfcd3c1fb16062f91914d6de47081
