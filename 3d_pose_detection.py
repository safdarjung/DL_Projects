import cv2
from cvzone.HandTrackingModule import HandDetector
import socket #for sending data using UDP protocol

width, height = 400, 400

cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

detector = HandDetector(detectionCon=0.8, maxHands=1)
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    _, frame = cap.read()
    # (x,y,z) * 21 landmarks which would be sent to unity
    hands,img = detector.findHands(frame)

    data = []
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        # print(lmList)

        # in unity 0,0,0 is at bottom right rather than top left
        for lm in lmList:
            data.extend([lm[0],-(height-lm[1]),lm[2]])

        # print(data)
        soc.sendto(str.encode(str(data)), serverAddressPort)
    cv2.imshow("Frame", img)

    key = cv2.waitKey(1)
    if key == 27:
        break