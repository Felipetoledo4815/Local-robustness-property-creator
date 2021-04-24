import cv2 as cv
import numpy as np
import matplotlib.image as mpimg


global counter
counter = 0

global coords 
coords = []

global resized

def shadeRegion(coords, bound):
    print(coords)
    print(resized.shape)
    top_left = coords[0]
    top_right = coords[1]
    lower_left = coords[3]
    lower_right = coords[2]

    color = ''
    if bound == "up":
        color = (255 ,255 ,255)
        bound = 'ub'
    else:
        color = (0, 0 , 0)
        bound = 'lb'

    # top left clockwise -> selection
    max_j  = lower_left[1]
    j = top_left[1]
    while j < max_j:
        for i in range(top_left[0], top_right[0]):
            resized[j][i] = color
        j += 1
    filename = 'generated_properties/dave_small_' + bound + '0.npy'
    x = cv.cvtColor(resized, cv.COLOR_BGR2RGB)
    x = np.moveaxis(x, -1, 0)
    np.save(filename, x)
    cv.imshow("resized image", resized)



def mousePoints(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        global counter
        counter += 1
        global coords
        if(counter <= 4):
            coords.append((x, y))
        else:
            shadeRegion(coords=coords, bound='low')
            shadeRegion(coords=coords, bound='up')



def main():
    global resized
    img = cv.imread('original_images/san_mateo.jpg')
    resized = cv.resize(img, dsize=(100, 100))
    print(resized.shape)
    x = cv.cvtColor(resized, cv.COLOR_BGR2RGB)
    x = np.moveaxis(x, -1, 0)
    np.save('generated_properties/dave_small_orig_img0.npy', x)
    cv.imshow("resized image", resized)
    cv.setMouseCallback("resized image", mousePoints)
    cv.waitKey(0)

if __name__ == "__main__":
    main()