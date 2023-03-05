import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)

offset = 20
imgSize = 300
while True:
  success, img = cap.read()
  hands, img = detector.findHands(img)
  if hands:
        # Hand 1
        hand1 = hands[0]
        #bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        x, y, w1, h1 = hand1['bbox']
        #centerPoint1 = hand1['center']  # center of the hand cx,cy
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop1 = img[y - offset:y + h1 + offset, x - offset:x + w1 + offset]
        
        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            x, y, w2, h2 = hand2['bbox']
            imgCrop2 = img[y - offset:y + h2 + offset, x - offset:x + w2 + offset]
            cv2.imshow("ImageCrop2", imgCrop2)
            # Calculate bounding box for both hands
            x_min, y_min, x_max, y_max = 10000, 10000, -1, -1
            for hand in hands:
                x_min = min(x_min, hand['bbox'][0])
                y_min = min(y_min, hand['bbox'][1])
                x_max = max(x_max, hand['bbox'][0] + hand['bbox'][2])
                y_max = max(y_max, hand['bbox'][1] + hand['bbox'][3])
            # Crop image
            imgCrop3 = img[y_min - offset :y_max + offset, x_min - offset:x_max + offset]
            cv2.imshow("ImageCrop3", imgCrop3)
        imgCropShape = imgCrop1.shape
        imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop1
        cv2.imshow("ImageCrop1", imgWhite)
  cv2.imshow("image", img)
  cv2.waitKey(1)