
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
color_thresholds = [(30, 100, 15, 127, 15, 127), # ball
              (30, 100, -64, -8, -32, 32), # yellow goal
              (0, 30, 0, 64, -128, 0)]  # orange goal
pixels_threshold=50
area_threshold=50
margin = 10
x_ema = None
y_ema = None
def colorDetectedByCamera(img):
   
    return "no"

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
