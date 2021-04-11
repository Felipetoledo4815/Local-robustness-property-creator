import cv2
import numpy as np

def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

img = cv2.imread('imgs/speed_limit.jpeg')

cv2.imshow("original image", img)

cv2.setMouseCallback("original image", mousePoints)

cv2.waitKey(0)