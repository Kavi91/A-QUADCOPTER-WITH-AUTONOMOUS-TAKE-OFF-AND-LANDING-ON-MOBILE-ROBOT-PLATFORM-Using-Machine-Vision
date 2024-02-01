import cv2
import numpy as np
import threading
import serial
import math

def nothing(x):
    pass

# Initialize camera
camera = cv2.VideoCapture(0)
width, height = 704, 576
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Create trackbars for tuning
cv2.namedWindow('image')
hh, hl, sh, sl, vh, vl = 'Hue High', 'Hue Low', 'Saturation High', 'Saturation Low', 'Value High', 'Value Low'
cv2.createTrackbar(hl, 'image', 0, 179, nothing)
cv2.createTrackbar(hh, 'image', 0, 179, nothing)
cv2.createTrackbar(sl, 'image', 0, 255, nothing)
cv2.createTrackbar(sh, 'image', 0, 255, nothing)
cv2.createTrackbar(vl, 'image', 0, 255, nothing)
cv2.createTrackbar(vh, 'image', 0, 255, nothing)

# Function for serial communication
def quadMovement(directionX, directionY):
    # Serial communication logic here
    pass

def Storage(quad_X, quad_Y):
    t1 = threading.Thread(target=quadMovement, args=(quad_X, quad_Y))
    t1.start()
    t1.join()

# Main loop
while True:
    _, frame = camera.read()

    # Read values from trackbars
    hul, huh = cv2.getTrackbarPos(hl, 'image'), cv2.getTrackbarPos(hh, 'image')
    sal, sah = cv2.getTrackbarPos(sl, 'image'), cv2.getTrackbarPos(sh, 'image')
    val, vah = cv2.getTrackbarPos(vl, 'image'), cv2.getTrackbarPos(vh, 'image')

    # Define arrays for minimum and maximum HSV values
    rangeMin = np.array([hul, sal, val], np.uint8)
    rangeMax = np.array([huh, sah, vah], np.uint8)

    # Image processing
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgErode = cv2.erode(imgThresh, None, iterations=5)
    blurred = cv2.GaussianBlur(imgErode, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        if len(approx) >= 4 and len(approx) <= 6:
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = 0.8 <= aspectRatio <= 1.2

            if keepDims and keepSolidity and keepAspectRatio:
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)
                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                Storage(cX, cY) # Assuming Storage function handles serial communication

    cv2.imshow('image', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.release()
cv2.destroyAllWindows()
