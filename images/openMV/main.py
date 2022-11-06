import sensor, image, time
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()
t1 = time.time()
while(True):
	clock.tick()
	img = sensor.snapshot()
	if time.time() -t1 > 2:
		sensor.snapshot().save("example" + str(t1) + ".jpg")
		t1 = time.time()
	print(clock.fps())