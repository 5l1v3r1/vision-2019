# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from networktables import NetworkTables
import numpy as np


def nothing(x):
    pass

display = 1
ip = "127.0.0.1"

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (300, 300)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(300, 300))

# allow the camera to warmup
time.sleep(0.1)

if(display == 1):
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

NetworkTables.initialize(server = ip)
datatable = NetworkTables.getTable("datatable")


# capture frames from the camera
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image - this array
    # will be 3D, representing the width, height, and # of channels
    frame = image.array
    # frame = frame[...,::-1]
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if(display == 1):
        cv2.imshow("Video Capture",frame)
    # cargo lower_green = np.array([0,203,0])
    # cargo upper_green = np.array([178,255,219])
    lower_green = np.array([170,203,170]) # 227,235,226 old values
    upper_green = np.array([255,255,255]) # 255,255,254 old values
    test_image = frame

    # cv2.imshow('Test',test_image)x
    # resizedImage = cv2.resize(test_image,(300,300))
    resizedImage = test_image
    resizedImage = resizedImage[125:300, 0:300]

    # cv2.imshow('Resized',resizedImage)

    veryMaskedImage = cv2.inRange(resizedImage,lower_green,upper_green)
    if(display == 1):
        cv2.imshow('test',veryMaskedImage)
        cv2.imshow('RRR',resizedImage)
    # cv2.imshow('Gray',grayImage)

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
    if(display == 1):
        cv2.imshow('Masked Image',maskedImage)
    contourImage, contours, hierarchy = cv2.findContours(veryMaskedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #cv2.CHAIN_APPROX_SIMPLE)
    contourIndexes =  []
    contourCounter = 0
    for contour in contours:
        area =  cv2.contourArea(contour)
        if(area > 125):
            contourIndexes.append(contourCounter)
        contourCounter += 1
     # print(contourIndexes)
    if(len(contourIndexes) >= 2):
        cnt = contours[contourIndexes[-1]]
        cnt2 = contours[contourIndexes[-2]]
        cv2.drawContours(resizedImage,[cnt],0,(255,0,0),4)
        cv2.drawContours(resizedImage,[cnt2],0,(255,0,0),4)
        x,y,w,h = cv2.boundingRect(cnt) 
        x2,y2,w2,h2 = cv2.boundingRect(cnt2)
        midPoint = (int)((x+x2+w2)/2)
       # print(midPoint)
        cv2.line(resizedImage,(midPoint,0),(midPoint,300), (0,0,255))
        cv2.line(resizedImage,(0,150),(300,150), (0,0,255))
        
        
        cameraHorizAngle = 60
        pixelToAngle = 300/cameraHorizAngle
        angles = []
        moc = 150 # moc stands for middle of the camera
        distanceToTurn = 0
        if(moc-midPoint >= 1):
            distanceToTurn = moc-midPoint
            pixelToAngle = -pixelToAngle
        else:
            distanceToTurn = midPoint-moc
            
             
        angleToTurn = int(distanceToTurn/pixelToAngle)
        print(angleToTurn)
        
        
        if(datatable.getBoolean('visionTrigger', False) == True):
            print("i got a message ")
            print('Angle : ' + str(angleToTurn))
            datatable.putNumber('angle',angleToTurn)
        
    if(display == 1):
        cv2.imshow('Filled Image',resizedImage)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    keyPressed = cv2.waitKey(1)
    if keyPressed == 27:
        break