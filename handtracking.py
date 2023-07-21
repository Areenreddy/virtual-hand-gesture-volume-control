import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
ctime = 0
ptime = 0

while True:
    sucess,img = cap.read()
    rgb_image = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for handmarks in results.multi_hand_landmarks:

            for ids,lm in enumerate(handmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(h*lm.y)

                if ids ==4:
                    cv.circle(img,(cx,cy),25,(255,0,255),cv.FILLED)


            mpdraw.draw_landmarks(img,handmarks,mphands.HAND_CONNECTIONS)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    cv.putText(img,str(int(fps)),(10,80),cv.FONT_HERSHEY_PLAIN,3,(225,0,225),2)

    cv.imshow("video",img)
    if cv.waitKey(20) & 0xFF== ord('d'):
        break
    

cv.destroyAllWindows()