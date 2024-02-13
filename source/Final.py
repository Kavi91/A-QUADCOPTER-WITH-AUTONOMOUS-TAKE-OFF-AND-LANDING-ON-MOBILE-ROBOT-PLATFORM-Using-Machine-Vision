'''
Created on Oct 31, 2016
Quadcopter Landing Algorithm opencv 2.4.11 and python 2.7

"A Quadcopter with automated Take-off and Landing on mobile robot platform"
A group project by  B.A.S Sandaruwan , S.Mithun & Rathnayake R.M.K.M
M.Eng(hons) in Electrical and Electronic Engineering,Faculty of Aces,Shiffield Hallam Univeristy,United Kingdom.

@author: Kavinda Rathnayake
'''
import cv2.cv as cv
import cv2
import numpy as np
import time
import threading
from time import sleep
import serial

#ser = serial.Serial('COM6', 9600)
ser = serial.Serial('COM8', 115200)
try: 
    ser.close()
    ser.open()
     
except Exception as e :
     
    print "error open serial port: " + str(e)
    exit()

def quadMovement(directionX,directionY):
    
    value_1 = str(directionX)
    value_2 = str(directionY)
    
    ser.write("A")
    ser.write(value_1)
    ser.write(",")
    ser.write(value_2)
    ser.write(",")
    ser.write("1212")
    ser.write(",?#")
    print ser.readline() 
  
                    
def Storage(quad_X,quad_Y):
    
    t1 = threading.Thread(target = quadMovement, args = (quad_X, quad_Y))
    t1.start()
    t1.join()
    
def nothing(x):
    
    pass

Hmin = 0
Hmax = 11
Smin = 195
Smax = 255
Vmin = 51
Vmax = 255
  
rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)
    
minArea = 50

width = 704
height = 576

centroid = height/2
 
centerimit = 50 

cv.NamedWindow('image', cv2.WINDOW_NORMAL)
cv.NamedWindow("Erode", cv2.WINDOW_NORMAL)


camera = cv2.VideoCapture(0)

hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'

cv2.createTrackbar(hl, 'image',0,179,nothing)
cv2.createTrackbar(hh, 'image',0,179,nothing)
cv2.createTrackbar(sl, 'image',0,255,nothing)
cv2.createTrackbar(sh, 'image',0,255,nothing)
cv2.createTrackbar(vl, 'image',0,255,nothing)
cv2.createTrackbar(vh, 'image',0,255,nothing)

if camera.isOpened():
        
        
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

while True:
    
  
    (grabbed, frame) = camera.read()
    status = "Searching the Object"

    if not grabbed:
        
        print "live feed has stopped"
        
        while 1:
            
            ser.write("XXX?#")
        
        break

    
    track_frame=cv2.GaussianBlur(frame,(5,5),0)
    hsv=cv2.cvtColor(track_frame, cv2.COLOR_BGR2HSV)
    
    hul=cv2.getTrackbarPos(hl, 'image')
    huh=cv2.getTrackbarPos(hh, 'image')
    sal=cv2.getTrackbarPos(sl, 'image')
    sah=cv2.getTrackbarPos(sh, 'image')
    val=cv2.getTrackbarPos(vl, 'image')
    vah=cv2.getTrackbarPos(vh, 'image')
    
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(frame,frame, mask =mask)
    
#     rangeMin = np.array([hul, sal, val], np.uint8)
#     rangeMax = np.array([huh, sah, vah], np.uint8)
    
    imgHSV = cv2.cvtColor(frame,cv2.cv.CV_BGR2HSV)    
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgErode = cv2.erode(imgThresh, None, iterations = 5)   
    blurred = cv2.GaussianBlur(imgErode, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    
    moments = cv2.moments( imgErode, True)
    
    if moments['m00'] >= minArea:
        x = moments['m10'] / moments['m00']
        y = moments['m01'] / moments['m00']
                   

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    
    for c in cnts:
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

        
        if len(approx) >= 4 and len(approx) <= 6:
            
            
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            
            
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            
            if keepDims and keepSolidity and keepAspectRatio:
                
                
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)
                status_1 = "Target is clear"
                status_2 = "Following the object"
                
                M = cv2.moments(approx)
                area = round(M['m00'])
               
                                                                                          
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                
                
                cv2.line(frame, (startX, cY), (endX, cY), (255, 0, 0), 2)
                cv2.line(frame, (cX, startY), (cX, endY), (255, 0, 0), 2)
                cv2.putText(frame,status_2, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 51), 2)
                cv2.putText(frame,"X: " + str(cX), (600, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 2)
                cv2.putText(frame,"Y: "+ str(cY), (700, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 2)
                
                
                Storage(cX, cY)
                
                if area:
                    cv2.putText(frame,str(area), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(210, 0, 255), 2)
                
            else:
                
                
                cv2.putText(frame,status, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2)
                ser.write("YYY?#")
                print "Searching for the extraction point"
                
                
    
    cv2.imshow('image', res)
    cv2.imshow("Frame", frame)
    cv2.imshow("Erode",blurred)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()