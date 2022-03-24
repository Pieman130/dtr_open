from pupil_apriltags import Detector
import cv2
from time import sleep

vid = cv2.VideoCapture(0)

#detector = Detector(families='tag16h5')
detector = Detector()
while True:
    ret, frame = vid.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    x = int(img.shape[0]/2)
    y = int(img.shape[1]-500)
    res = detector.detect(img, estimate_tag_pose=False)
    if ret:
        try:
            #print("Tag Id: ", res[0].tag_id)
            cv2.putText(frame, "Decoded Tag Id: {}".format(res[0].tag_id), (x,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)
            cv2.imshow("Image", frame)
            cv2.waitKey(0)
            break
        except:
            pass
    else:
        print("Fail")
        sleep(0.25)
cv2.imwrite("decoded_tag{}.jpg".format(res[0].tag_id),frame)
