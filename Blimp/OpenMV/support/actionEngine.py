
from processing import data
processedData = data

def getNextStep(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    global processedData    

    print(" action engine! ir data: " + str(processedData.irData))
    print(" action engine! img: " + str(processedData.colorDetected))
    output = 0
    print("get next step")
    return output



def executeNextStep():
    output = 0
    print("execute next step")
        

def searchForBall():
    global processedData


def searchForGoal():
    global processedData

def moveToBall():
    global processedData

def moveToGoal():
    global processedData

def score():
    global processedData
