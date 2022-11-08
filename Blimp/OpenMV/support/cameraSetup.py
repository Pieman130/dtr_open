class OpenMVcamera:
    def __init__(self,camera):
        self.camera = camera
        self.camera.reset()

        self.camera.set_pixformat(self.camera.RGB565)
        self.camera.set_framesize(self.camera.QVGA)
        #self.camera.set_framesize(self.camera.QQVGA) #needed for april tag detections
        self.camera.skip_frames(20)
        self.camera.set_auto_gain(False) # must be turned off for color tracking
        self.camera.set_auto_whitebal(True)
        #self.camera.set_auto_exposure(False)
    def snapshot(self):
        img = self.camera.snapshot()
        return img

