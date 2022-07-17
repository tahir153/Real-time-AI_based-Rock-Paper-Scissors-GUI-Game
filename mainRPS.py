import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False

score = [0,0]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success , img = cap.read()

    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled = imgScaled[:,80:480]

    imgBG[234:654,795:1195] = imgScaled
    final = cv2.resize(imgBG, (380, 0), None, 0.925, 0.925)


    # Find Hand
    hands, img = detector.findHands(final)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(final,str(int(timer)),(565,395),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),7)

            if timer > 2:
                stateResult = True
                timer = 0

                if hands:
                    Human_playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        Human_playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        Human_playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        Human_playerMove = 3

                    randomNumber = random.randint(1,3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                    final = cvzone.overlayPNG(final,imgAI,(130,270))

                    # Human Player Move
                    if (Human_playerMove == 1 and randomNumber == 3) or \
                        (Human_playerMove == 2 and randomNumber == 1) or \
                        (Human_playerMove == 3 and randomNumber == 2):
                        score[1] += 1
                    # AI Player Move
                    if (Human_playerMove == 3 and randomNumber == 1) or \
                        (Human_playerMove == 1 and randomNumber == 2) or \
                        (Human_playerMove == 2 and randomNumber == 3):
                        score[0] += 1


    if stateResult:
        final = cvzone.overlayPNG(final,imgAI,(130,270))
    cv2.putText(final, str(score[0]), (380, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(final, str(score[1]), (1030, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", final)
    # cv2.imshow("Image", img)
    # cv2.imshow("Scaled", imgScaled)

    key = cv2.waitKey(1)
    if key == ord("s"):
        startGame = True
        initialTime = time.time()
        stateResult = False
