
import sensor, image # for stupid example
import time
import math

threshold_index = 1 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0),
              (50, 100,-20,20, 30, 100)] # generic_yellow_thresholds] # generic_blue_thresholds


def colorDetectedByCamera(img)-> str:
    colorDetected = 'other'
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
            colorDetected = 'green'

    return colorDetected

def lookForAprilTag(img):
    print("in look for april tag")
    class TagInfo:
        def __init__(self):
            self.foundIt = 0
            self.tags = None
            self.rotation = None

    tagsFound = TagInfo()
    
    foundIt = 0
    
    for tag in img.find_apriltags(): # defaults to TAG36H11 without "families".        
        tagsFound.foundIt = 1 
        tagsFound.tags = tag 
        tagsFound.rotation = (180 * tag.rotation()) / math.pi    
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)

    print("found april tag?: " + str(tagsFound.foundIt))

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
