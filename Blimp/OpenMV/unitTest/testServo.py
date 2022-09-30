import pyb

import time

SERVO_PWM_ID = 3
servo = pyb.Servo(SERVO_PWM_ID)

SERVO_OPEN = 15
SERVO_CLOSED = 65

while(True):
    print("open")
    servo.angle(SERVO_OPEN,500)

    time.sleep(3)

    print("close")
    servo.angle(SERVO_CLOSED,500)


    time.sleep(3)
