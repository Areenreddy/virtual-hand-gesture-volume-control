import cv2 as cv
import mediapipe as mp
import time 


class handdetector():
    def __init__(self,mode = False,maxhands = 2,modelcomplex=1,detectioncon = 0.5,trackingcon = 0.5):
        self.modelcomplex=modelcomplex
        self.mode = mode
        self.maxhands = maxhands
        self.detectioncon = detectioncon
        self.trackingcon = trackingcon
        
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxhands,self.modelcomplex,self.detectioncon,self.trackingcon)
        self.mpdraw = mp.solutions.drawing_utils

    def findhands(self,img,draw = True):

        rgb_image = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_image)

        if self.results.multi_hand_landmarks:
            for handmarks in self.results.multi_hand_landmarks:
                if draw :
                    self.mpdraw.draw_landmarks(img,handmarks,self.mphands.HAND_CONNECTIONS)

        return img
    
    def findposition(self,img,handno= 0,draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for ids,lm in enumerate(myhand.landmark):
                    h,w,c = img.shape
                    cx,cy = int(lm.x*w),int(h*lm.y)
                    lmlist.append([ids,cx,cy])
                    if draw:
                        cv.circle(img,(cx,cy),10,(255,0,255),cv.FILLED)
        return lmlist
    

def main():
    cap = cv.VideoCapture(0)
    ctime = 0
    ptime = 0
    detector = handdetector()
    while True:
        sucess,img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.findposition(img,draw=False)
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(img,str(int(fps)),(10,80),cv.FONT_HERSHEY_PLAIN,3,(225,0,225),2)
        cv.imshow("video",img)
        if cv.waitKey(20) & 0xFF== ord('d'):
            break

    cv.destroyAllWindows()
if __name__ == "__main__":
    main()