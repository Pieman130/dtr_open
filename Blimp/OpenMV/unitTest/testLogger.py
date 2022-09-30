import sys
import pathlib

#WHEN I TESTED THIS I HAD IT DIRECTLY IN SUPPORT FOLDER.  TO TEST FROM HERE NEED TO ADD /SUPPORT FOLDER.  Didn't figure out how to do that.
#baseDir = str(pathlib.Path(__file__).parent.resolve()) # Get directory of main
#import os
#os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))


#pathDir = baseDir + '..\\support'
#sys.path.append()``


import logger


#logger.setLevel_silent()

class TestPrint():
    def __init__(self):
        pass
    def print(self):
        logger.log.error('error')
        logger.log.warning('warning')
        logger.log.heartbeat('heartbeat')
        logger.log.info('info')
        logger.log.verbose('verbose')
        logger.log.debugOnly('debugOnly')
        logger.log.silly('silly')        

tp = TestPrint()


print("===SILENT===")
logger.log.setLevel_silent()
tp.print()


print("===ERROR===")
logger.log.setLevel_error()
tp.print()

print("===WARNING===")
logger.log.setLevel_warning()
tp.print()

print("===HEARTBEAT===")
logger.log.setLevel_heartbeat()
tp.print()


print("===INFO===")
logger.log.setLevel_info()
tp.print()



print("===VERBOSE===")
logger.log.setLevel_verbose()
tp.print()


print("===SILLY===")
logger.log.setLevel_silly()
tp.print()


print("===DEBUG ONLY===")
logger.log.setLevel_debugOnly()
tp.print()







