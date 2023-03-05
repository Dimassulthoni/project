import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)

offset = 20
while True:
  success, img = cap.read()
  hands, img = detector.findHands(img)
  if hands:
        # Hand 1
        hand1 = hands[0]
        #bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        x, y, w1, h1 = hand1['bbox']
        #centerPoint1 = hand1['center']  # center of the hand cx,cy
        imgCrop1 = img[y - offset:y + h1 + offset, x - offset:x + w1 + offset]
        cv2.imshow("ImageCrop1", imgCrop1)
        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            x, y, w2, h2 = hand2['bbox']
            imgCrop2 = img[y - offset:y + h2 + offset, x - offset:x + w2 + offset]
            cv2.imshow("ImageCrop2", imgCrop2)
            w3 = w1+w2
            h3 = h1+h2
            imgCrop3 = img[y - offset:y + h3 + offset, x - offset:x + w3 + offset]
            cv2.imshow("ImageCrop3", imgCrop3)
            #centerPoint2 = hand2['center']  # center of the hand cx,cy
            # Find Distance between two Landmarks. Could be same hand or different hands
            # length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
            #cv2.imshow("ImageCrop3", imgCrop1, imgCrop2)
  cv2.imshow("image", img)
  cv2.waitKey(1)