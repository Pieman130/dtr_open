
import mavlink_messages
from processing import data
import externalSensors

processedData = data

msgToSend = None

def getNextStep(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    global processedData    

    print(" action engine! ir data: " + str(processedData.irData))
    print(" action engine! img: " + str(processedData.colorDetected))
    output = 0
    print("get next step")

    print(processedData.foundAprilTag)
    if (processedData.foundAprilTag):
        moveForwardFull()
    else:
        stopForwardMotion()

    return output




        

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
    global msgToSend

    print("stop moving forward")
    
    minValue = 1100
    ch = (0,0,minValue,0,0,0,0,0)

    msgToSend = mavlink_messages.mvlink_ch_overide(1,ch)
    

def moveForwardFull():
    global msgToSend
    # mavlink_messages 
    # #2 = lift
    # #3 = throttle
    # #4 = up

    fullValue = 1900
    midValue = 1500
    barelyOn = 1200
    minValue = 1100

    ch = (0,0,fullValue,0,0,0,0,0)
    msgToSend = mavlink_messages.mvlink_ch_overide(1,ch)

    print("forward ahead!")


def executeNextStep():
    global msgToSend
    output = 0
    print("execute next step")
    externalSensors.pixracerWrite(msgToSend)