import sys
import pathlib

# add Logger path to python path
baseDir = pathlib.Path(__file__).parent 
supportPath = str((baseDir  / "../support/").resolve())
sys.path.append(supportPath)

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







