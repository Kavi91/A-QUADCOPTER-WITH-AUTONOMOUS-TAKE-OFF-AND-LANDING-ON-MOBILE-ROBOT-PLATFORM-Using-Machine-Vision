'''
Created on Nov 8, 2016

@author: Kavinda
'''
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

ser = serial.Serial('COM8', 115200)

try: 
    ser.close()
    ser.open()
     
except Exception, e:
     
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
    
    #ser.flushInput()
    #ser.flushOutput()
    #print ser.readline() 
  
                    
def Storage(quad_X,quad_Y):
    
    t1 = threading.Thread(target = quadMovement, args = (quad_X, quad_Y))
    t1.start()
    t1.join()
    
def nothing(x):
    
    pass

#red
# Hmin = 0
# Hmax = 179 
# Smin = 43
# Smax = 255
# Vmin = 253
# Vmax = 255

#green
Hmin = 35
Hmax = 90
Smin = 57
Smax = 255
Vmin = 172
Vmax = 255

#blue
# Hmin = 87
# Hmax = 101
# Smin = 129
# Smax = 255
# Vmin = 255
# Vmax = 255
  
rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)
    
minArea = 18000

width =704
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
    
    start_time = time.time()
  
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
    imgErode = cv2.erode(imgThresh, None, iterations = 1)   
    blurred = cv2.GaussianBlur(imgErode, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    
    moments = cv2.moments( imgErode, True)
    area = moments['m00']
    
    if area >= 1000:
        
        status_1 = "Target is clear"
        status_2 = "Following the object"
        
        x = int(moments['m10']) / int(moments['m00'])
        y = int(moments['m01']) / int(moments['m00'])
                   
        cv2.circle(frame, (int(x), int(y)), 10, (255, 0, 0), -1)
        
        cv2.putText(frame,status_1, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 51), 2)
        cv2.putText(frame,status_2, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 51), 2)
        cv2.putText(frame,"X: " + str(x), (600, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 2)
        cv2.putText(frame,"Y: "+ str(y), (700, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 2)
        cv2.putText(frame,str(area), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(210, 0, 255), 2)
        
        Storage(x, y)
        
    else:
                
                
        cv2.putText(frame,status, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2)
        ser.write("YYY?#")
        #print "Searching for the extraction point"
                
                
    
    cv2.imshow('image', res)
    cv2.imshow("Frame", frame)
    cv2.imshow("Erode",blurred)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
        
camera.release()
cv2.destroyAllWindows()

