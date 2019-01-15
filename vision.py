# -*- coding: utf-8 -*-
import cv2
import numpy as np

def nothing(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow('Colorbars')
# Assign strings for ease of coding
bh='Blue High'
bl='Blue Low'
gh='Green High'
gl='Green Low'
rh='Red High'
rl='Red Low'
wnd='Colorbars'
# Begin Creating trackbars for each BGR value
cv2.createTrackbar(bl, wnd, 0,   255, nothing)
cv2.createTrackbar(bh, wnd, 0,   255, nothing)
cv2.createTrackbar(gl, wnd, 0,   255, nothing)
cv2.createTrackbar(gh, wnd, 0,   255, nothing)
cv2.createTrackbar(rl, wnd, 0,   255, nothing)
cv2.createTrackbar(rh, wnd, 0,   255, nothing)
    
# cargo lower_green = np.array([0,203,0])
# cargo upper_green = np.array([178,255,219])
lower_green = np.array([227,235,226])
upper_green = np.array([255,255,254])
test_image = cv2.imread('images/rocket/rocket_image2.jpg')

# cv2.imshow('Test',test_image)x
resizedImage = cv2.resize(test_image,(300,300))

# cv2.imshow('Resized',resizedImage)

veryMaskedImage = cv2.inRange(resizedImage,lower_green,upper_green)
cv2.imshow('test',veryMaskedImage)
cv2.imshow('RRR',resizedImage)
# cv2.imshow('Gray',grayImage)

while True:
    ret, frame = cap.read()
    cv2.imshow("Video Capture",frame)

    bLow  = cv2.getTrackbarPos(bl, wnd)
    bHigh = cv2.getTrackbarPos(bh, wnd)
    gLow  = cv2.getTrackbarPos(gl, wnd)
    gHigh = cv2.getTrackbarPos(gh, wnd)
    rLow  = cv2.getTrackbarPos(rl, wnd)
    rHigh = cv2.getTrackbarPos(rh, wnd)
    
    rgbLow=np.array([bLow,gLow,rLow])
    rgbHigh=np.array([bHigh,gHigh,rHigh])
    
    maskedImage = cv2.inRange(frame, rgbLow, rgbHigh)
    kernel = np.ones((10,10),np.uint8)
    openedImage = cv2.morphologyEx(maskedImage, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((30,30),np.uint8)
    openedImage = cv2.morphologyEx(openedImage, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('Masked Image',maskedImage)
    contourImage, contours, hierarchy = cv2.findContours(veryMaskedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #cv2.CHAIN_APPROX_SIMPLE)
    contourIndexes =  []
    contourCounter = 0
    for contour in contours:
        area =  cv2.contourArea(contour)
        if(area > 200):
            contourIndexes.append(contourCounter)
        contourCounter += 1
    print(contourIndexes)
    if(len(contourIndexes) > 2):
        cnt = contours[contourIndexes[-1]]
        cnt2 = contours[contourIndexes[-2]]
        cv2.drawContours(resizedImage,[cnt],0,(255,0,0),4)
        cv2.drawContours(resizedImage,[cnt2],0,(255,0,0),4)
        x,y,w,h = cv2.boundingRect(cnt) 
        x2,y2,w2,h2 = cv2.boundingRect(cnt2)
        midPoint = (x+x2+w2)/2
        print(midPoint)
        cv2.line(resizedImage,(midPoint,0),(midPoint,300), (255,255,255))
        cv2.line(resizedImage,(0,150),(300,150), (255,255,255))
    
    # cv2.line(resizedImage,(x,0),(x,300), (255,255,255))
    # cv2.line(resizedImage,(x2,0),(x2,300), (255,255,255))

    cv2.imshow('Filled Image',resizedImage)

    keyPressed = cv2.waitKey(1)
    if keyPressed == 27:
        break
cv2.destroyAllWindows() # Destroy the windows and close the program
