from gpiozero import Servo, Motor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

servo = Servo(17, pin_factory=PiGPIOFactory())

motor = Motor(27,22,enable=23)

for i in range(60):
    if i < 15:
        motor.forward(i/15)
        servo.value=i/15
    elif i < 30:
        motor.forward(-i/15+2.0)
        servo.value=-i/15+2.0
    elif i <45:
        motor.backward(i/15-2.0)
        servo.value=-i/15+2.0
    else:
        motor.backward(-i/15+4.0)
        servo.value=i/15-4.0
    sleep(0.25)
