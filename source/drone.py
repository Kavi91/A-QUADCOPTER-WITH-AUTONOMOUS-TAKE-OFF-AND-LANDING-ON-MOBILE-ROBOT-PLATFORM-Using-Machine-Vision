'''
Created on Jul 28, 2016

@author: Kavinda
'''

# import the necessary packages
import cv2.cv as cv
import argparse
import cv2
import numpy as np
from time import sleep
import serial


ser = serial.Serial('COM6', 9600)# Establish the connection on a specific port

#---------------------------------------------------------------------
#  CONFIGURING THE SERVO
#---------------------------------------------------------------------
#def setServo(servodirection):
    
#    value = servodirection
#    ser.write(str(value)) # Convert the decimal number to ASCII then send it to the Arduino
#    print ser.readline() # Read the newest output from the Arduino
#    sleep(0.1) # Delay for one tenth of a second
      
              
#--------------------------------------------------------------------------

# servo = 100
# servoMin = 30
# servoMax = 180
#  
# servodirection1 = 'a'
# servodirection2 = 'b'
# servodirection3 = 'c'
# servodirection4 = 'd'
# servodirection5 = 'z'
# 
# servodirection6 = 'e' 
# servodirection7 = 'f'
# servodirection8 = 'g'
# servodirection9 = 'h'
# servodirection10 = 'i'

#center of axis
#centroy = altura/2


#limit the cennter
#may = 50 #24


# #Pattern white
# Hmin = 150
# Hmax = 255 
# Smin = 150
# Smax = 255
# Vmin = 150
# Vmax = 255

# Hmin = 42
# Hmax = 92
# Smin = 62
# Smax = 255
# Vmin = 63
# Vmax = 235


#Pattern RED
Hmin = 0
Hmax = 179 
Smin = 131
Smax = 255
Vmin = 126
Vmax = 255

minArea = 50

# Parameters capture image HV
width = 1024
height = 768

rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)

cv.NamedWindow("Erosao")
camera = cv2.VideoCapture(1)

if camera.isOpened():
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)


# keep looping
while True:
    # grab the current frame and initialize the status text
    (grabbed, frame) = camera.read()
    status = "Searching the Object"

    if not grabbed:
        break

    # convert the frame to HSV
    imgHSV = cv2.cvtColor(frame,cv2.cv.CV_BGR2HSV)    
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgErode = cv2.erode(imgThresh, None, iterations = 3)
    
    #edged = cv2.Canny(frame, 50, 150)
    
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(imgErode, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    
    moments = cv2.moments( imgErode, True)
    
    if moments['m00'] >= minArea:
        x = moments['m10'] / moments['m00']
        y = moments['m01'] / moments['m00']
          
        cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
    
# # If the limit is greater than the distance from which is taken centralized
#         if (y - centroy) >= may:
#             servo = servo - 3
#             setServo(servodirection1)
#           
# # set limit for minor ...
#         elif (centroy - y) >= may:
#             servo = servo + 3
#             setServo(servodirection2)
#             
#         else:
#      
#             setServo(servodirection5)     
#         if servo < servoMin:
#             servo = servoMin
#             setServo(servodirection3)
#             
#         if servo > servoMax:
#             servo = servoMax
#             setServo(servodirection4)
#             
#         
#             
#         #If the limit is greater than the distance from which is taken centralized
#         if (x - centroy) >= may :
#             servo = servo - 3
#             setServo(servodirection6)
#             
#             
# # set limit for minor ...
#         elif (centroy - x) >= may:
#             servo = servo + 3
#             setServo(servodirection7) 
#              
#         else:
#      
#             setServo(servodirection10)        
#    
#             
#         if servo < servoMin:
#             servo = servoMin
#             setServo(servodirection8)
#             
#         if servo > servoMax:
#             servo = servoMax
#             setServo(servodirection9)   
    
    
    

    # find contours in the edge map
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

        # ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            # compute the bounding box of the approximated contour and
            # use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            # compute the solidity of the original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            # compute whether or not the width and height, solidity, and
            # aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            # ensure that the contour passes all our tests
            if keepDims and keepSolidity and keepAspectRatio and moments['m00'] >= minArea:
                # draw an outline around the target and update the status
                # text
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)
                status = "Target is clear"

                # compute the center of the contour region and draw the
                # crosshairs
                M = cv2.moments(approx)
                area = round(M['m00'])
                print area
                
                
#                 if moments['m00'] >= minArea:
        
                x = moments['m10'] / moments['m00']
                y = moments['m01'] / moments['m00']
          
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
                
                
                
                
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                
                cv2.line(frame, (startX, cY), (endX, cY), (255, 0, 0), 2)
                cv2.line(frame, (cX, startY), (cX, endY), (255, 0, 0), 2)

    # draw the status text on the frame
    cv2.putText(frame,status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2)
    
    
    #cv2.putText(frame,str(area),(20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 2)
    
    # show the frame and record if a key is pressed
    cv2.imshow("Frame", frame)
    cv2.imshow("Erosao",blurred)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()