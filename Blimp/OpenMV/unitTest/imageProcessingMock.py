import logger
import imageProcessing
def colorDetectedByCamera(img)-> str:
    logger.log.verbose("mock color detected by camera")
    return "other"

def lookForAprilTag(img):
    logger.log.verbose("mock look for april tag")
    return imageProcessing.TagInfo()


def family_name(tag):
    logger.log.verbose("family name")    
    return "TAG16H5"
