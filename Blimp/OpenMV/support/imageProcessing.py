
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

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
color_thresholds = [(30, 100, 15, 127, 15, 127), (30, 100, -64, -8, -32, 32), (0, 30, 0, 64, -128, 0)]
pixels_threshold=50
area_threshold=50
margin = 10
x_ema = None
y_ema = None
width = 0
def colorDetectedByCamera(img):
    blobs = 0
    #search for ball in img
    biggestball = [0,0,0,0] #[x, y, width, height]
    currentball = [0,0,0,0] #[x, y, width, height]
    for blobs in img.find_blobs([color_thresholds[0]], pixels_threshold = pixels_threshold, area_threshold = area_threshold, merge=True, margin = margin):
        currentball = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        if currentball[2] > biggestball[2]:
            biggestball = currentball
    if blobs != 0:
        if x_ema == None:
            x_ema = EMA(currentball[0], 1 - 0.7)
        else:
            x_ema.update(currentball[0])
        if y_ema == None:
            y_ema = EMA(currentball[1], 1 - 0.7)
        else:
            y_ema.update(currentball[1])
        dataClasses.ProcessedData.ballx = x_ema
        dataClasses.ProcessedData.bally = y_ema
        width = biggestball[2]
    #NEED TO DISCUSS HOW TO PICK GOAL
    if dataClasses.ProcessedData.goalColorChoice == "yellow":
        threshold = 1
    else:
        threshold = 2
    #search for yellow goal
    for blob in img.find_blobs([color_thresholds[threshold]], pixels_threshold = pixels_threshold, area_threshold = area_threshold, merge=True, margin = margin):
        currentgoal = [blob.cx(), blob.cy(), blob.rect()[2], blob.rect()[3]]
        if abs(160 - (currentgoal[0])) < abs(160 - (closestgoal[0])): #instead of current[0], use pythagorean theorem to find closest ball
            closestgoal = currentgoal
    if blob != 0:
        dataClasses.ProcessedData.goalColorDetected = True
        dataClasses.ProcessedData.goalx = closestgoal[0]
        dataClasses.ProcessedData.goaly = closestgoal[1]
        dataClasses.ProcessedData.goalskew = closestgoal[3]/closestgoal[4]
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
