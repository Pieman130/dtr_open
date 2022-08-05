
import mavlink_messages
from processing import data
processedData = data

def getNextStep(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    global processedData    

    print(" action engine! ir data: " + str(processedData.irData))
    print(" action engine! img: " + str(processedData.colorDetected))
    output = 0
    print("get next step")

    if (processedData.foundAprilTag):
        moveForwardFull()
    else:
        stopForwardMotion()

    return output



def executeNextStep():
    output = 0
    print("execute next step")
        

def searchForBall():
    # sensors: camera, lidar
    global processedData


def searchForGoal():
    global processedData

def moveToBall():
    global processedData

def moveToGoal():
    global processedData

def score():
    global processedData

def stopForwardMotion():
    print("stop moving forward")
    ch=(0,0,0,0,0,0,0,0)
    mavlink_messages.mvlink_ch_overide(1,ch)

def moveForwardFull():
    # mavlink_messages 
    # #2 = lift
    # #3 = throttle
    # #4 = up
    ch=(0,0,0,0,0,0,0,0)
    mavlink_messages.mvlink_ch_overide(1,ch)
    print("forward ahead!")