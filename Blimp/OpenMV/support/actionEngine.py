def getNextStep(): # https://github.com/mavlink/c_library_v1/blob/master/checksum.h
    from processing import ProcessedData

    print(" action engine! ir data: " + str(ProcessedData.irData))
    print(" action engine! img: " + str(ProcessedData.colorDetected))
    output = 0
    print("get nexst step")
    return output


def executeNextStep():
    output = 0
    print("execute next step")
        