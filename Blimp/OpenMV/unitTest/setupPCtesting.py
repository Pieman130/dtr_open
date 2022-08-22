import sys

def setupImportsForNoOpenMVoperations():
    import hardwareMock
    hardware = hardwareMock

    import commsMock
    comms = commsMock
    
    sys.path.append('C:\DroneRepos\DTRRepo\Blimp\OpenMV\support')