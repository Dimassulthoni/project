import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)

offset = 20
imgSize = 300

while True:
  success, img = cap.read()
  hands, img = detector.findHands(img)
  if hands:
        # Hand 1
        if len(hands) == 1:
            hand1 = hands[0]
            #bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            x, y, w, h = hand1['bbox']
            #centerPoint1 = hand1['center']  # center of the hand cx,cy
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop1 = img[y - offset:y + h + offset, x - offset:x + w + offset]
            
            imgCropShape = imgCrop1.shape
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop1, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop1, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
            #imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop1
            cv2.imshow("ImageCrop1", imgWhite)
        else :
            # Hand 2
            hand2 = hands[1]
            x, y, w, h = hand2['bbox']
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop2 = img[y - offset:y + h + offset, x - offset:x + w + offset]
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
                imgCropShape = imgCrop3.shape
                aspectRatio = h / w
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop3, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop3, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    #imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop3
                cv2.imshow("ImageCrop1", imgWhite)
                    #cv2.imshow("ImageCrop3", imgCrop3)
                
        
  cv2.imshow("image", img)
  cv2.waitKey(1)