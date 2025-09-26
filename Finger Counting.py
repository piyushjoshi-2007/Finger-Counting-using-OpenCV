import cv2 as cv
import time
import os 
import HandtrackingModule as htm

face_cascade=cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv.VideoCapture(0,cv.CAP_DSHOW)
pTime=0
detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]


while(True):
    ret,frame=cap.read()
    face=face_cascade.detectMultiScale(frame,1.7,3)
    for(x,y,w,h) in face:
        cv.rectangle(frame,(x,y,w,h),(0,0,255),2)
   

    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame,draw=False)
    # print(lmList)
    if len(lmList) !=0:
        fingers=[]
    #thumb (rifgt hand)  for left hand just change the sign of < with > in this only
        if lmList[tipIds[0]][1] <  lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

#for other four fingures
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)  

        # print(fingers) 
        totalfing=fingers.count(1)
        a=str(totalfing)
        # print(totalfing)
        cv.putText(frame,a + "Fingers",(150,450),cv.FONT_HERSHEY_PLAIN,4,(5,0,255),3)
#fps
    cTime=time.time()
    fps= 1/(cTime - pTime)
    pTime=cTime
    cv.putText(frame,f'FPS:{int(fps)}',(520,70),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv.putText(frame,f'FACES:{int(len(face))}',(150,50),cv.FONT_HERSHEY_PLAIN,2,(255,250,250),3)
    cv.imshow("IMAGE",frame)
#to end the cam
    if cv.waitKey(1) & 0xFF== ord("q"):
        break



cap.release()
cv.destroyAllWindows()