import sensor, image, time, math, ustruct, sys, pyb, pid
from pyb import USB_VCP, Pin, Timer, Servo

ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led
ledBlue = pyb.LED(3) # Initiates the blue led
ledIR = pyb.LED(4)

threshold_index = 1
auto_mode = True

thresholds = [(60, 82, -48, -11, -128, 127), #yellow 0
              (0, 70, -59, -12, -10, 54), #green 1
              (17, 100, 14, 70, 34, 127)] #orange 2

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 200)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(auto_mode) # must be turned off for color tracking (I ignored this and kept it on)
clock = time.clock()

class EMA:
    def __init__(self, value, alpha = 0.85):
        self.value = value
        self.alpha = alpha
        self.alpha_compl = 1 - alpha
    def update(self, value):
        self.value = self.alpha * self.value + self.alpha_compl * value
    def get_value(self):
        return self.value
# these are the coordinates of the center of the goal
goalx_ema = None
goaly_ema = None
SQerror = 0

# these are the coordinates of the largest ball
x_ema = None
y_ema = None
rect_ema = None #This is bounding box of ball, used to determine what is the closest

#misc. variables
alpha_rect = .85 # alpha value of the rectangle that bounds the ball
goal_alpha = .85 # alpha value of the rectangle that bounds the goal

goal_xerror = 0 # Distance in pixels away from the goal horizontally
goal_yerror = 0 # Distance in pixels away from the goal vertically

ball_xerror = 0 # Distance in pixels away from the ball horizontally
ball_yerror = 0 # Distance in pixels away from the ball vertically

dist_ball = 0 #do not use
dist_goal = 0 #do not use

ledGreen.off()
ledRed.off()
ledBlue.off()
ledIR.off()

def find_ball():
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
                x_ema = EMA(current[0], 1 - 0.7)
                rect_ema = [EMA(r[0], alpha_rect), EMA(r[1], alpha_rect), EMA(r[2], alpha_rect), EMA(r[3], alpha_rect)]
                y_ema = EMA(current[1], 1 - 0.7)
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
            ball_xerror = round(x_ema.get_value()) - 160
            ball_yerror = round(y_ema.get_value()) - 120

def find_yellow_goal():
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
    goal_xerror = 160 - round(goalx_ema.get_value())
    goal_yerror = round(goaly_ema.get_value()) - 120

def find_orange_goal():
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
    goal_xerror = 160 - round(goalx_ema.get_value())
    goal_yerror = round(goaly_ema.get_value()) - 120

def printall():
    print("[%d, %d]\n\r" % (x_ema.get_value(), y_ema.get_value()), end=' ')
    print("Ball is %d inches away\n\r" % dist_ball)
    print("[%d, %d]" % (round(goalx_ema.get_value()), round(goaly_ema.get_value())), end=' ')
    print("Goal is %d inches away\n\r" % dist_goal)
    print("Percentage of goal seen %d \n\r" % SQerror)
    print(clock.fps())

while(True):
    try:
        clock.tick()
        img = sensor.snapshot()# take photo
        img.draw_cross(160, 120, [236, 232, 26]) #draw cross in center of screen
        find_ball()
        #find_orange_goal()
        #find_yellow_goal()
        print(clock.fps())
        print("X Error to goal is: " + str(goal_xerror))
        print("Y Error to goal is: " + str(goal_yerror))
        print("X Error to ball is: " + str(ball_xerror))
        print("Y Error to ball is: " + str(ball_yerror))
        #if (dist_ball != 0):
            #printall()
    except RuntimeError:
        pass

