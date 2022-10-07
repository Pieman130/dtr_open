#Works for Windows and MacOS, will not work for Linux
import os
from distutils.dir_util import copy_tree

if os.name == 'posix': #Unix-like machines
    currDir = os.path.dirname(os.path.realpath(__file__))

    if os.uname().sysname == 'Darwin': #MacOs
        if os.path.exists("/Volumes/NO NAME"):
            to_directory = "/Volumes/NO NAME"

        elif os.path.exists("/Volumes/IU_DTR_RED"):
            to_directory = "/Volumes/IU_DTR_RED"
            
        elif os.path.exists("/Volumes/IU_DTR_BLUE"):
            to_directory = "/Volumes/IU_DTR_BLUE"

        elif os.path.exists("/Volumes/IU_DTR_DEV"):
            to_directory = "/Volumes/IU_DTR_DEV"
        else:
            raise Exception("OpenMV Camera Volume Name Not Valid!")

        from_directory = currDir +"/support"
            
    else:
        pass #TODO fix for Linux machines


else: #Windows machines
    currDir = os.path.dirname(__file__)
    to_directory = "E:/"
    from_directory = currDir + "\support"

copy_tree(from_directory, to_directory)



