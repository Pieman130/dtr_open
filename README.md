More info in wiki: [DTR Wiki](https://github.iu.edu/DTR/dtr/wiki)

`blimpy.py` is the main Blimp script

`IMU_test.py` to run simple tests to ensure BNO055 IMU is functioning

`LIDAR_test.py` tests for TFMini lidar using UART connection

`manual_control.py` to operate blimp with only PS3 controller (no autonomy)  Note: deadman switch is disabled 

**NOTE: the BNO055 library requires two updates:**
1) Ensure software I2C is enabled and HW I2C is disabled on the raspberry pi
	1) modify `/boot/config.txt` to include this line:
	
	`dtoverlay=i2c-gpio,bus=3,i2c_gpio_sda=23,i2c_gpio_scl=24`
	
	2) comment this line out if not already done:

	`dtparam=i2c_arm=on`

2) You may need to modify `bno055.py` to add support for software i2c bus.  On line 196 `self._bus = smbus.SMBus(1)` change the 1 to a 3
