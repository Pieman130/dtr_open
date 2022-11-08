
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


THRESHOLDS = [(64, 100, -36, -11, 8, 127), #yellow 0
              (0, 70, -59, -12, -10, 54), #green 1
              (35, 62, 29, 93, 35, 98)] #orange 2

class ImageProcessing():
    def __init__(self):
        self.goalx_ema = None
        self.goaly_ema = None
        self.SQerror = 0

        # data on selected ball (all three are instances of EMA)
        self.x_ema = None
        self.y_ema = None
        self.rect_ema = None #This is bounding box of ball, used to determine what is the closest

        #misc. variables
        self.alpha_rect = .85 # alpha value of the rectangle that bounds the ball
        self.goal_alpha = .85 # alpha value of the rectangle that bounds the goal
        self.ball_alpha = .85 # alpha value of the centroid of the ball

        self.goal_xerror = 0 # Distance in pixels away from the goal horizontally from center (int)
        self.goal_yerror = 0 # Distance in pixels away from the goal vertically from center (int)

        self.ball_xerror = 0 # Distance in pixels away from the ball horizontally (int)
        self.ball_yerror = 0 # Distance in pixels away from the ball vertically (int)

        self.dist_ball = 0 # (float)
        self.dist_goal = 0 # (float)


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
                    self.rect_ema = [EMA(r[0], self.alpha_rect), 
                                    EMA(r[1], self.alpha_rect), 
                                    EMA(r[2], self.alpha_rect), 
                                    EMA(r[3], self.alpha_rect)]
                    self.y_ema = EMA(biggest[1], self.ball_alpha)
                else:
                    self.x_ema.update(biggest[0])
                    self.y_ema.update(biggest[1])
                    self.rect_ema[0].update(r[0])
                    self.rect_ema[1].update(r[1])
                    self.rect_ema[2].update(r[2])
                    self.rect_ema[3].update(r[3])
                if (self.rect_ema[2].get_value() != 0):
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
            counter = 0
            #dataClasses.data.yellowGoalIsFound = 0
            if blobs: #goal like object detected
                for blob in blobs:
                    dataClasses.data.yellowGoalIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
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
                dataClasses.data.goal_yellow_goal_yerror = round(self.goaly_ema.get_value()) - (img.height()/2)

            else: #nothing that looks like a goal was detected
                dataClasses.data.yellowGoalIsFound = 0
                dataClasses.data.goal_yellow_xerror = None
                dataClasses.data.goal_yellow_goal_yerror = None
                logger.log.verbose("Yellow Goal Not Found!")
                return
        else:
            logger.log.warning("No Image Passed to ImageProcessing!")

    def find_orange_goal(self,img):
        if img != None:
            blobs = img.find_blobs([THRESHOLDS[2]], pixels_threshold=3, area_threshold=12, merge=True, margin=10)
            biggest = [160,120,0,0] #[cx, cy, width, height]
            counter = 0
            #dataClasses.data.orangeGoalIsFound = 0
            if blobs: #goal like object detected
                for blob in blobs:
                    dataClasses.data.orangeGoalIsFound = 1
                    current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
                    img.draw_rectangle(blob.rect())
                    #img.draw_cross(current[0], current[1])
                    counter = counter + 1
                    width = current[2]
                    height = current[3]
                    self.SQerror = width/height
                    if current[3] > biggest[3]:
                        biggest = current
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

            else: #nothing that looks like a goal was detected
                dataClasses.data.orangeGoalIsFound = 0
                dataClasses.data.goal_orange_xerror = None
                dataClasses.data.goal_orange_goal_yerror = None
                logger.log.verbose("Orange Goal Not Found!")
                return
        else:
            logger.log.warning("No Image Passed to ImageProcessing!")

