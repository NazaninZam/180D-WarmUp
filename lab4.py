# -*- coding: utf-8 -*-
"""
Sources:
    https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
    https://www.geeksforgeeks.org/real-time-object-color-detection-using-opencv/
"""
import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0) #set up camera 


while True:
    # each frame
    ret, frame = cap.read()
    
    #convert BGR to HSV, comment out for RBG
    imgHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #define color you want in HSV
    low_blue=np.array([100, 50, 50])
    up_blue=np.array([130, 255, 255])
  
    
    blue_mask = cv.inRange(imgHSV,up_blue,low_blue)
    
    #define color you want in BRG comment out for HSV
    #low_blue = np.array([255,0,0])
    #up_blue = np.array([255,200,200])
    #blue_mask=cv.inRange(frame,up_blue,low_blue)
    

    contours, _ =  cv.findContours(blue_mask, 1, 2)
        
    if len(contours)>0:
        blue_area = max(contours, key=cv.contourArea)
        if cv.contourArea(blue_area) > 1000: 
            (x,y,w,h) = cv.boundingRect(blue_area)
            cv.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)

    cv.imshow('color_detect', frame)
    
    if cv.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyWindow('color_detect')