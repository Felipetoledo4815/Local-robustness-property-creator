import cv2
import numpy as np

def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

# resize to 100 x 100
img = cv2.imread('imgs/01. san_mateo.jpg')

cv2.imshow("original image", img)

cv2.setMouseCallback("original image", mousePoints)

cv2.waitKey(0)