import cv2 as cv
import time 
import numpy as np
import handtrackingmodule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam, hcam = 640,480

cap = cv.VideoCapture(0)

cap.set(3,wcam)
cap.set(4,hcam)

detector = htm.handdetector(detectioncon=0.7)

ctime = 0
ptime =0
volbar = 200
volper =0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volrange=volume.GetVolumeRange()
minvol = volrange[0]
maxvol = volrange[1]




while True:
    sucess,img = cap.read()
    img = detector.findhands(img)
    lmlist = detector.findposition(img,draw=False)
    if len(lmlist) != 0 :
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cv.circle(img,(x1,y1),10,(255,255,0),cv.FILLED)
        cv.circle(img,(x2,y2),10,(255,255,0),cv.FILLED)
        cv.line(img,(x1,y1),(x2,y2),(0,255,100),3)
        cv.circle(img,((x2+x1)//2,(y2+y1)//2),10,(255,255,0),cv.FILLED)
        length = math.hypot((x1-x2),(y1-y2))


        vol = np.interp(length,[20,250],[minvol,maxvol])
        volbar = np.interp(length,[20,250],[200,50])
        volper = np.interp(length,[20,250],[0,100])

        volume.SetMasterVolumeLevel(vol, None)

        # print(vol)

        if length < 50 :
            cv.circle(img,((x2+x1)//2,(y2+y1)//2),10,(0,255,0),cv.FILLED)
        cv.rectangle(img,(50,50),(75,200),(0,255,0),3)
        cv.rectangle(img,(50,int(volbar)),(75,200),(0,255,0),cv.FILLED)
        cv.putText(img,str(int(volper)),(50,250),cv.FONT_HERSHEY_PLAIN,4,(255,0,0),3)

        
    

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    cv.putText(img,str(int(fps)),(10,80),cv.FONT_HERSHEY_PLAIN,4,(255,60,140),3)

    cv.imshow("image",img)
    if cv.waitKey(20) & 0xFF== ord('d'):
        break

cv.destroyAllWindows()