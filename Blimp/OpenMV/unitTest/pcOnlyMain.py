import pathlib
import sys
unitDir = pathlib.Path(__file__).parent
baseDir = pathlib.Path(unitDir).parent
supportDir = (baseDir / "support/").resolve()
print(unitDir, supportDir)

#sys.path.append(str(unitDir))
sys.path.append(str(supportDir))


import hardwareMock
hardware = hardwareMock

import commsMock
comms = commsMock

import mainWorker

mainWorker.run()