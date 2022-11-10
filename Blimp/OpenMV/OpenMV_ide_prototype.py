import sensor, image, time, math, ustruct, sys, pyb, pid
from pyb import USB_VCP, Pin, Timer, Servo

ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led
ledBlue = pyb.LED(3) # Initiates the blue led


threshold_index = 1
auto_mode = True
flip = False

thresholds = [(30, 100, 15, 127, 15, 127), #0 generic_red_thresholds
              (8, 85, -66, -14, -76, 59), #1 generic_green_thresholds (25, 105, -69, -3, -37, 37)
              (0, 30, 0, 64, -128, 0), #2 generic_blue_thresholds
              (91, 69, -85, -30, 0, 127), #3 pistachio mix can
              (25, 47, -58, -5, -23, 7), #4 green ink shapes
              (0, 59, 17, 27, 12, 60)] #5 red ink shapes

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(flip)
sensor.set_vflip(flip)
sensor.skip_frames(time = 200)
sensor.set_auto_gain(auto_mode) # must be turned off for color tracking
sensor.set_auto_whitebal(auto_mode) # must be turned off for color tracking
clock = time.clock()

class EMA:
    def __init__(self, value, alpha = 0.5):
        self.value = value
        self.alpha = alpha
        self.alpha_compl = 1 - alpha
    def update(self, value):
        self.value = self.alpha * self.value + self.alpha_compl * value
    def get_value(self):
        return self.value
# these are the coordinates of the center of the goal closest to the center of the screen
goalx_ema = None
goaly_ema = None
SQerror = 0

# these are the coordinates of the largest ball
x_ema = None
y_ema = None
rect_ema = None

#misc. variables
alpha_rect = 1 - 0.1
h1 = None
b1 = None

ledGreen.off()
ledRed.off()
ledBlue.off()

dist_ball = 0
dist_goal = 0

def find_ball():
    blobs = img.find_blobs([thresholds[1]], pixels_threshold=50, area_threshold=50, merge=True,  margin = 10)
    biggest = [0,0,0,0] #[x, y, width, height]
    global x_ema
    global y_ema
    global rect_ema
    global alpha_rect
    global h1
    global b1
    global dist_ball
    #if len(blobs) == 0:
        #print("-1, -1")
    for blob in blobs:
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        if current[2] > biggest[2]:
            biggest = current
            if x_ema == None:
                x_ema = EMA(current[0], 1 - 0.7)
            else:
                x_ema.update(current[0])
            if y_ema == None:
                y_ema = EMA(current[1], 1 - 0.7)
            else:
                y_ema.update(current[1])
            r = blob.rect()
            if rect_ema == None:
                rect_ema = [EMA(r[0], alpha_rect), EMA(r[1], alpha_rect), EMA(r[2], alpha_rect), EMA(r[3], alpha_rect)]
            else:
                rect_ema[0].update(r[0])
                rect_ema[1].update(r[1])
                rect_ema[2].update(r[2])
                rect_ema[3].update(r[3])
            if b1 == None:
                b1 = r[2]
                h1 = 1
            if (rect_ema[2].get_value() != 0):
                dist_ball = 22/(math.tan((rect_ema[2].get_value() * .22125)/2)) #rect_ema[2].getvalue() gives ball width, use equation for pixel width to meters away
            #img.draw_rectangle(blob.rect())
            img.draw_rectangle([round(ema.get_value()) for ema in rect_ema], 2)
            img.draw_string(round(rect_ema[0].get_value()),round(rect_ema[1].get_value()), " Ball", [0, 0, 255], mono_space = False)
            #img.draw_cross(blob.cx(), blob.cy())
            img.draw_cross(round(x_ema.get_value()), round(y_ema.get_value()), 2)

def find_goal():
    blobs = img.find_blobs([thresholds[5]], pixels_threshold=5, area_threshold=5, merge=True, margin=5)
    biggest = [-1,-1,0,0] #[cx, cy, width, height]
    counter = 0
    global dist_goal
    global goalx_ema
    global goaly_ema
    global SQerror
    #if len(blobs) == 0:
        #print("No Goals in Sight")
    for blob in blobs:
        current = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        img.draw_rectangle(blob.rect())
        img.draw_cross(current[0], current[1])
        counter = counter + 1
        width = current[2]
        height = current[3]
        SQerror = width/height
        img.draw_string(blob.rect()[0], blob.rect()[1],"Goal",[0, 0, 255] , mono_space = False)
        #print("Counter", counter)
        #print("Position:", current[0], current[1])
        #print("Distance:", distance, "inches")
        #print("Width", width)
        #print("Height:", height)
        #print("Square error:", round(SQerror, 1))
        if abs(160 - (current[0])) < abs(160 - (biggest[0])):
            biggest = current
            goalindex = counter
            #print("Goal selected", goalindex)
    if goalx_ema == None:
        goalx_ema = EMA(biggest[0], 1 - 0.1)
    else:
        goalx_ema.update(biggest[0])
    if goaly_ema == None:
        goaly_ema = EMA(biggest[1], 1 - 0.1)
    else:
        goaly_ema.update(biggest[1])
    if (biggest[3] != 0):
        dist_goal = 42 / math.tan((biggest[3] * .23166/2)) # change parameters to determine distance from goal with known values, biggest[3] is height of goal
    img.draw_cross(round(goalx_ema.get_value()), round(goaly_ema.get_value()), color=[0,0,0])

def full_scan():
    print("")

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
        img = sensor.snapshot()
        img.draw_cross(160, 120, [236, 232, 26])
        find_ball()
        find_goal()
        if (dist_ball != 0):
            printall()
    except RuntimeError:
        pass

