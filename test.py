import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
from collections import Counter


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2, detectionCon=0.90)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

labels = ["A", "B", "C", "D", "E", "F", "G", "H",
          "I", "J", "K", "L", "M", "N", "O", "P", 
          "Q", "R", "S", "T", "U", "V", "W", "X", 
          "Y", "Z"]

predictions_per_second = []
start_time = 0


while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    
    if hands:
        # Hand 1
        if len(hands) == 1:
            hand1 = hands[0]
            #bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            x, y, w, h = hand1['bbox']
            #centerPoint1 = hand1['center']  # center of the hand cx,cy
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            imgCropShape = imgCrop.shape
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
        
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                
        else :
            # Hand 2
            hand2 = hands[1]
            x, y, w, h = hand2['bbox']
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            # Calculate bounding box for both hands
            x_min, y_min, x_max, y_max = 10000, 10000, -1, -1
            for hand in hands:
                x_min = min(x_min, hand['bbox'][0])
                y_min = min(y_min, hand['bbox'][1])
                x_max = max(x_max, hand['bbox'][0] + hand['bbox'][2])
                y_max = max(y_max, hand['bbox'][1] + hand['bbox'][3])
            # Crop image
                imgCrop = img[y_min - offset :y_max + offset, x_min - offset:x_max + offset]
                imgCropShape = imgCrop.shape
                aspectRatio = h / w
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                    
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    
        prediction, index = classifier.getPrediction(imgWhite, draw=False)
        predictions_per_second.append(tuple(labels[index]))
        
        current_time = time.time()
        
        # Jika sudah mencapai 1 detik, cari modus dari prediksi
        if current_time - start_time >= 1:
            prediction_counts = Counter(predictions_per_second)
            mode_prediction = max(prediction_counts, key=prediction_counts.get)
            print("Mode prediction:", mode_prediction)

            # Reset daftar prediksi per detik dan waktu mulai
            predictions_per_second = []
            start_time = time.time()
        
        cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        #cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)