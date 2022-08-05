
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
    # taken from find_apriltags_1.py example in open mv drop down example files
    foundIt = 0
    for tag in img.find_apriltags(): # defaults to TAG36H11 without "families".
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        foundIt = 1
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)
    
    return foundIt


def lookForAprilTagStupid():
        
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
    sensor.skip_frames(time = 2000)
    sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
    sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
    clock = time.clock()

    # Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

    # The apriltag code supports up to 6 tag families which can be processed at the same time.
    # Returned tag objects will have their tag family and id within the tag family.

    tag_families = 0
    tag_families |= image.TAG16H5 # comment out to disable this family
    tag_families |= image.TAG25H7 # comment out to disable this family
    tag_families |= image.TAG25H9 # comment out to disable this family
    tag_families |= image.TAG36H10 # comment out to disable this family
    tag_families |= image.TAG36H11 # comment out to disable this family (default family)
    tag_families |= image.ARTOOLKIT # comment out to disable this family

    # What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
    # a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
    # is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
    # rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
    # reason to use the other tags families just use TAG36H11 which is the default family.


    clock.tick()
    img = sensor.snapshot()
    
    foundIt = 0
    
    for tag in img.find_apriltags(): # defaults to TAG36H11 without "families".        
        foundIt = 1
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)

    print("found april tag?: " + str(foundIt))


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