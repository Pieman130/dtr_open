#Works for Windows and MacOS, will not work for Linux
import os
from distutils.dir_util import copy_tree

if os.name == 'posix': #Unix-like machines
    currDir = os.path.dirname(os.path.realpath(__file__))

    if os.uname().sysname == 'Darwin': #MacOs
       to_directory = "/Volumes/NO NAME"
       from_directory = currDir +"/support"
    else:
        pass #TODO fix for Linux machines

else: #Windows machines
    currDir = os.path.dirname(__file__)
    to_directory = "E:/"
    from_directory = currDir + "\support"

copy_tree(from_directory, to_directory)



