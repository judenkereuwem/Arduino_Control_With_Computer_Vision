import cv2
import time
import os
import serial
import HandTrackingModule as htm

ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

wCam, hCam = 640, 480

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)
overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)

print(len(overLayList))
pTime = 0

detector = htm.handDetector(detectionCon = 0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        #thump
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)       
              

        totalFingers = fingers.count(1)
        print(totalFingers)
        if totalFingers == 0:
            ser.write(b'A')
        elif totalFingers == 1:
            ser.write(b'B')
        elif totalFingers == 2:
            ser.write(b'C')
        elif totalFingers == 3:
            ser.write(b'D')
        elif totalFingers == 4:
            ser.write(b'E')
        elif totalFingers == 5:
            ser.write(b'F')

        h, w, c = overLayList[totalFingers].shape
        img[0:h, 0:w] = overLayList[totalFingers-1]

        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (50, 390), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
ser.close()
