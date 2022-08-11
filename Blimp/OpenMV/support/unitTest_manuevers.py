import maneuvers
from maneuvers import GoForward
from maneuvers import ExitCriteria


activeManuever = None

myExitCriteria = ExitCriteria()
myExitCriteria.add("timeClock",5)

duration = 5
speed = 0.5
forward = GoForward(duration,speed,myExitCriteria)


while not forward.isExitCriteriaMet():
    forward.executeNextStep()



print('test')

