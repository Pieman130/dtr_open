import board
import busio
import adafruit_bno055
from time import sleep

i2c = busio.I2C(board.SCL,board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

for i in range(50):
    print("Accel (m/s^2): ", sensor.acceleration)
    print("Euler angle: ", sensor.euler)
    sleep(1)


