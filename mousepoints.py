import cv2 as cv
import numpy as np
import matplotlib.image as mpimg


global counter
counter = 0

global coords 
coords = []

global resized

def shadeRegion(coords, bound, output, name):
    global resized 

    print(coords)
    print(resized.shape)
    top_left = coords[0]
    top_right = coords[1]
    lower_right = coords[2]
    lower_left = coords[3]
    
    color = 0
    if bound == "up":
        color = (255, 255, 255)
        bound = 'ub'
    else:
        color = (0, 0, 0)
        bound = 'lb'

    pts = np.array([top_left,top_right,lower_right,lower_left])
    shape = cv.polylines(resized, [pts],True,(0, 0, 0))
    cv.fillPoly(resized, [pts], color)
    # cv.imshow("poly lines", resized)

    x = cv.cvtColor(resized, cv.COLOR_BGR2RGB)
    # filename = 'generated_properties/dave_small_' + bound + '0.npy'
    filename = output + bound + name +'.npy'
    x = np.moveaxis(x, -1, 0)
    np.save(filename, x)
    # cv.namedWindow("final image " + bound,cv.WINDOW_NORMAL)
    # cv.imshow("final image " + bound, resized)
    # cv.resizeWindow("final image " + bound, 500, 500)

    # top left clockwise -> selection
    # max_j  = lower_left[1]
    # j = top_left[1]
    # while j < max_j:
    #     for i in range(top_left[0], top_right[0]):
    #         resized[j][i] = color
    #     j += 1
    # filename = 'generated_properties/dave_small_' + bound + '0.npy'
    # x = cv.cvtColor(resized, cv.COLOR_BGR2RGB)
    # x = np.moveaxis(x, -1, 0)
    # np.save(filename, x)
    # cv.imshow("resized image", resized)



def mousePoints(event, x, y, flags, params):
    global counter
    global coords
    global resized
    if event == cv.EVENT_LBUTTONDOWN:
        counter += 1
        coords.append((x, y))
        if counter == 2:
            resized = cv.line(resized,coords[0],coords[1],(0,0,255),1)
            cv.imshow("resized image", resized)
        if counter == 3:
            resized = cv.line(resized,coords[1],coords[2],(0,0,255),1)
            cv.imshow("resized image", resized)
        if counter == 4:
            resized = cv.line(resized,coords[2],coords[3],(0,0,255),1)
            resized = cv.line(resized,coords[3],coords[0],(0,0,255),1)
            cv.imshow("resized image", resized)
    if event == cv.EVENT_MOUSEMOVE and 0 < len(coords) and len(coords) < 4:
        resized_tmp = resized.copy()
        resized_tmp = cv.line(resized_tmp,coords[counter-1],(x,y),(0,0,255),1)
        cv.imshow("resized image", resized_tmp)


def main(args):

    global resized
    global coords

    # img = cv.imread('original_images/san_mateo.jpg')
    img = cv.imread(args.img)
    resized = cv.resize(img, dsize=(100, 100))
    print(resized.shape)
    x = cv.cvtColor(resized, cv.COLOR_BGR2RGB)
    x = np.moveaxis(x, -1, 0)
    # np.save('generated_properties/dave_small_orig_img0.npy', x)
    np.save(args.output + 'orig_img' + args.name + '.npy', x)
    cv.namedWindow('resized image',cv.WINDOW_NORMAL)
    
    cv.imshow("resized image", resized)
    cv.resizeWindow('resized image', 500, 500)
    while(len(coords) < 4):
        cv.waitKey(1)
        cv.setMouseCallback("resized image", mousePoints)
    shadeRegion(coords=coords, bound='low', output=args.output, name=args.name)
    shadeRegion(coords=coords, bound='up', output=args.output, name=args.name)
    k = 0
    while (k != 27 and k != 113):
        print(k)
        k = cv.waitKey(0)
    cv.destroyAllWindows()
            

if __name__ == "__main__":
    main()