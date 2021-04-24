import cv2
import numpy as np


global counter
counter = 0

global coords 
coords = []

global resized

def shadeRegion(coords):
    print(coords)
    print(resized.shape)
    for i in range(coords[2][0], coords[3][0]):
        for j in range(coords[2][1], coords[3][1]):
            resized[j][i] = (0, 0, 0)
    cv2.imshow("resized image", resized)

def mousePoints(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global counter
        counter += 1
        global coords
        if(counter <= 4):
            coords.append((x, y))
        else:
            shadeRegion(coords=coords)

# resize to 100

img = cv2.imread('imgs/san_mateo.jpg')

resized = cv2.resize(img, (100, 100))

cv2.imshow("resized image", resized)

cv2.setMouseCallback("resized image", mousePoints)

cv2.waitKey(0)