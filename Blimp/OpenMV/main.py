# Untitled - By: timothy.woodbridge - Fri May 20 2022

import time

try: 
    import hardware
    import comms

except:
    import sys
    sys.path.append('C:\DroneRepos\DTRRepo\Blimp\OpenMV\unitTest')
    
    import hardwareMock
    hardware = hardwareMock

    import commsMock
    comms = commsMock
    sys.path.append('C:\DroneRepos\DTRRepo\Blimp\OpenMV\support')
                
   # import setupPCtesting
    #setupPCtesting.setupImportsForNoOpenMVoperations   


import processing
import actionEngine
import groundStation


def main() -> None:
    loopPause = 1
        
    hw = hardware.Hardware()

    com = comms.Comms(hw)    

    externalSensors.swInitialization(hw,com) 

    groundStation.swInitialization(com) 


    actionEngine.initialize()
    

    clock = time.clock()

    while(True):
        clock.tick()        

        time.sleep(loopPause)

        externalSensors.collectData()

        processing.parseSensorData()
                
        groundStation.sendStatusMessage()

       # actionEngine.updateState()

      #  actionEngine.getNextStep()

       # actionEngine.executeNextStep()               

        
main()
