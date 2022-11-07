 
class OpenMVcamera:
    def __init__(self,camera):
        self.camera = camera
        self.camera.reset()

        self.camera.set_pixformat(self.camera.RGB565)

        self.camera.set_framesize(self.camera.QVGA)
        #self.camera.set_framesize(self.camera.QQVGA) #needed for april tag detections

    # self.camera.skip_frames(2000)

    # needed for april tag finder
        self.camera.set_auto_gain(False)  # must turn this off to prevent image washout...

        self.camera.set_auto_whitebal(False)  # must turn this off to prevent image washout...   
        
    def snapshot(self):
        img = self.camera.snapshot()
        return img