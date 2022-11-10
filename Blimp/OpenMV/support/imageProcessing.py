from dataClasses import ProcessedData
import dataClasses
import logger
import math
from math import sqrt
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

THRESHOLDS = [(47, 77, -39, -13, 38, 93), #yellow 0
              (30, 100, -48, -13, -88, 127), #green 1
              (30, 100, 18, 88, 3, 66)] #orange 2


class ImageProcessing():

    def __init__(self):
        self.density_min = 100000
        self.density_max = 0


        #data on selected goals
        self.orange_goalx_ema = None
        self.orange_goaly_ema = None
        self.yellow_goalx_ema = None
        self.yellow_goaly_ema = None
        self.orange_SQerror = 0
        self.yellow_SQerror = 0

        self.goalx_ema = None
        self.goaly_ema = None
        self.SQerror = 0

        # data on selected ball (all three are instances of EMA)
        self.x_ema = None
        self.y_ema = None
        self.rect_ema = None #This is bounding box of ball, used to determine what is the closest

        # might be unused
        self.dist_ball = 0 # (float)
        self.dist_goal = 0 # (float)

        # data on selected ball (all three are instances of EMA)
        self.x_ema = None
        self.y_ema = None
        self.rect_ema = None #This is bounding box of ball, used to determine what is the closest
        # end might be unused

        #misc. variables
        self.alpha_rect = .85 # alpha value of the rectangle that bounds the ball
        self.goal_alpha = .85 # alpha value of the rectangle that bounds the goal
        self.ball_alpha = .85 # alpha value of the centroid of the ball

        self.orange_goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
        self.orange_goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)
        self.yellow_goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
        self.yellow_goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)

        self.ball_xerror = 0 # Distance in pixels away from the ball horizontally (int)
        self.ball_yerror = 0 # Distance in pixels away from the ball vertically (int)

    def find_ball(self,img):
        if img != None:
            blobs = img.find_blobs([THRESHOLDS[1]], pixels_threshold=50, area_threshold=50, merge=True,  margin = 10)
            biggest = [-1,-1,0,0] #[x, y, width, height]
            r = [0,0,0,0] #[x, y, width, height]
            dataClasses.data.ballIsFound = 0
            if blobs: #something that looks like a ball was detected
                for blob in blobs:
                    dataClasses.data.ballIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
                    if current[2] > biggest[2] and ((blob.density()/0.7854) > .65) and (current[2]/current[3]) < 2:
                        biggest = current
                        hold = (blob.density()/0.7854)
                        r = blob.rect()
                        if (hold < self.density_min):
                            self.density_min = hold
                        if (hold > self.density_max):
                            self.density_max = hold
                #print("Min " + str(self.density_min))
                #print("Max " + str(self.density_max))
                if biggest[0] != -1:
                    if self.x_ema == None:
                        self.x_ema = EMA(biggest[0], self.ball_alpha)
                        self.y_ema = EMA(biggest[1], self.ball_alpha)
                        self.rect_ema = [EMA(r[0], self.alpha_rect),
                                        EMA(r[1], self.alpha_rect),
                                        EMA(r[2], self.alpha_rect),
                                        EMA(r[3], self.alpha_rect)]
                    else:
                        self.x_ema.update(biggest[0])
                        self.y_ema.update(biggest[1])
                        self.rect_ema[0].update(r[0])
                        self.rect_ema[1].update(r[1])
                        self.rect_ema[2].update(r[2])
                        self.rect_ema[3].update(r[3])
                    if (self.rect_ema[2].get_value() != 0):
                        dataClasses.data.distanceToBall = 22/(math.tan((self.rect_ema[2].get_value()*.22125*0.01745329)/2)) #rect_ema[2].getvalue() gives ball width, use equation for pixel width to meters away
                    #img.draw_rectangle(blob.rect())
                    img.draw_rectangle([round(ema.get_value()) for ema in self.rect_ema], [0, 255, 0])
                    img.draw_string(round(self.rect_ema[0].get_value()),round(self.rect_ema[1].get_value()), "Ball", [0, 255, 0], mono_space = False)
                    #img.draw_cross(blob.cx(), blob.cy())
                    img.draw_cross(round(self.x_ema.get_value()), round(self.y_ema.get_value()), [0, 255, 0])
                    dataClasses.data.ball_xerror = round(self.x_ema.get_value()) - (img.width()/2)
                    dataClasses.data.ball_yerror = round(self.y_ema.get_value()) - (img.height()/2)
            else: #nothing that looks like a ball was detected
                dataClasses.data.ballIsFound = 0
                dataClasses.data.ball_xerror = None
                dataClasses.data.ball_yerror = None
                logger.log.verbose("No Ball Found!")
                # XXX return here right?
                return
        else:
            logger.log.warning("No Image Passed to ImageProcessing!")

    def find_yellow_goal(self,img):
        if img != None:
            blobs = img.find_blobs([THRESHOLDS[0]], pixels_threshold=10, area_threshold=12, merge=True, margin=5)
            biggest = [-1,-1,0,0] #[cx, cy, width, height]
            dataClasses.data.yellowGoalIsFound = 0
            if blobs: #goal like object detected
                for blob in blobs:
                    dataClasses.data.yellowGoalIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
                    minor = blob.minor_axis_line()
                    major = blob.major_axis_line()
                    width = sqrt((pow(minor[0] - minor[2], 2) + pow(minor[1] - minor[3], 2)))
                    height = sqrt((pow(major[0] - major[2], 2) + pow(major[1] - major[3], 2)))
                    current[2] = width
                    current[3] = height
                    if (width > biggest[3] and (blob.solidity()) < .65 and ((height/width) < 1.75)): #and (self.yellow_SQerror < 1.5) and (self.yellow_SQerror > .33):
                        majormax = major
                        minormax = minor
                        biggest = current
                        self.yellow_SQerror = height/width
                        print(self.yellow_SQerror)
                if biggest[0] != -1:
                    if self.yellow_goalx_ema == None:
                        self.yellow_goalx_ema = EMA(biggest[0], self.goal_alpha)
                        self.yellow_goaly_ema = EMA(biggest[1], self.goal_alpha)
                    else:
                        self.yellow_goalx_ema.update(biggest[0])
                        self.yellow_goaly_ema.update(biggest[1])
                    if (biggest[3] != 0):
                        dataClasses.data.dist_yellow_goal = (46/2)/math.atan(abs((biggest[3]*.23166*0.01745329))/2) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
                    img.draw_cross(round(self.yellow_goalx_ema.get_value()), round(self.yellow_goaly_ema.get_value()), color=[255, 255, 0])
                    img.draw_string(round(self.yellow_goalx_ema.get_value()), round(self.yellow_goaly_ema.get_value()),"Goal",[255, 255, 0] , mono_space = False)
                    dataClasses.data.goal_yellow_xerror = round(self.yellow_goalx_ema.get_value()) - (img.width()/2)
                    dataClasses.data.goal_yellow_yerror = round(self.yellow_goaly_ema.get_value()) - (img.height()/2)                    
            else: #nothing that looks like a goal was detected
                dataClasses.data.yellowGoalIsFound = 0
                dataClasses.data.goal_yellow_xerror = None
                dataClasses.data.goal_yellow_yerror = None
                logger.log.verbose("Yellow Goal Not Found!")
        logger.log.verbose("IMAGE PROCESSING_ yellow goal is: " + str(dataClasses.data.yellowGoalIsFound))
        

    def find_orange_goal(self,img):
        if img != None:
            blobs = img.find_blobs([THRESHOLDS[2]], pixels_threshold=3, area_threshold=20, merge=True, margin=0)
            biggest = [-1,-1,0,0] #[cx, cy, width, height]
            dataClasses.data.orangeGoalIsFound = 0
            if blobs: #goal like object detected
                for blob in blobs:
                    dataClasses.data.orangeGoalIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
                    minor = blob.minor_axis_line()
                    major = blob.major_axis_line()
                    width = sqrt((pow(minor[0] - minor[2], 2) + pow(minor[1] - minor[3], 2)))
                    height = sqrt((pow(major[0] - major[2], 2) + pow(major[1] - major[3], 2)))
                    current[2] = width
                    current[3] = height
                    if (width > biggest[3] and (blob.solidity()) < .65 and ((height/width) < 1.75)): # and self.orange_SQerror < 1.5 and self.yellow_SQerror > .75):
                        majormax = major
                        minormax = minor
                        biggest = current
                        self.orange_SQerror = height/width
                        print(self.orange_SQerror)
                if biggest[0] != -1:
                    img.draw_line(minormax)
                    img.draw_line(majormax)
                    if self.orange_goalx_ema == None:
                        self.orange_goalx_ema = EMA(biggest[0], self.goal_alpha)
                        self.orange_goaly_ema = EMA(biggest[1], self.goal_alpha)
                    else:
                        self.orange_goalx_ema.update(biggest[0])
                        self.orange_goaly_ema.update(biggest[1])
                    if (biggest[3] != 0):
                        dataClasses.data.dist_orange_goal = (46/2)/math.atan(abs((biggest[3]*.23166*0.01745329))/2) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
                    img.draw_cross(round(self.orange_goalx_ema.get_value()), round(self.orange_goaly_ema.get_value()), color=[255, 165, 0])
                    img.draw_string(round(self.orange_goalx_ema.get_value()), round(self.orange_goaly_ema.get_value()),"Goal" ,[255, 165, 0] , mono_space = False)
                    dataClasses.data.goal_orange_xerror = round(self.orange_goalx_ema.get_value()) -(img.width()/2)
                    dataClasses.data.goal_orange_yerror = round(self.orange_goaly_ema.get_value()) - (img.height()/2)
            else: #nothing that looks like a goal was detected
                dataClasses.data.orangeGoalIsFound = 0
                dataClasses.data.goal_orange_xerror = None
                dataClasses.data.goal_orange_yerror = None
                logger.log.verbose("Orange Goal Not Found!")
                return
        else:
            logger.log.warning("No Image Passed to ImageProcessing!")

        logger.log.verbose("IMAGE PROCESSING_ orange goal is: " + str(dataClasses.data.orangeGoalIsFound))
