import numpy as np

from utils import *
from imglib import *
from PIL import Image

path1 = '1/1/database/base_1_2_1.bmp'
path2 = '1/4/database/base_1_1_4.bmp'
path3 = '1/7/database/base_1_1_7.bmp'

img1 = getImg(path2)

def getULpos(img):
    if img.sum() == 0:
        return 0
    sizeX, sizeY = img.shape
    imgt = img.copy()
    sizeS = sizeX+sizeY-1
    URline_bol = np.empty([sizeS],dtype=bool)

    for i in reversed(range(sizeY-1)):
        imgt[i][1:] = np.logical_or(imgt[i][1:],imgt[i+1][:-1])
        URline_bol[sizeX+i] = imgt[i+1][-1]


    URline_bol[:sizeX] = imgt[0]

    pos = sizeS
    for i in range(sizeS):
        if imgt[0][i] !=0:
            pos = i
            break
    if pos == sizeS:
        print("It's empty!")
        return 0
    if pos < sizeY and pos < sizeX: 
        for i in range(pos+1):
            if img[pos-i][i]:
                return (pos-i,i)

        print('Wrong')
        return 0

    else:
        print("Oops!")

def detContour(img):
    '''
    new version, contour in white(empty) space
    '''

    DEBUG_OPT = True
    DEBUG_OPT = False

    Ox,Oy = getULpos(img)
    Oy -= 1
    sizeX,sizeY = img.shape
    contourList = []

    #      -X
    #       ^
    #       |
    # -Y<---O---> Y
    #       |
    #       V
    #       X

    
    dirList = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
    dirIdx = 3
    x,y = Ox,Oy
    contourList.append((x,y))
    mx,my = dirList[dirIdx]
    rotateCount = 0

    # import time

    mx,my = dirList[dirIdx]
    if DEBUG_OPT:
        print("Start point = ({:d},{:d}).".format(Ox,Oy))
        print("Direction = ({:d},{:d}).".format(mx,my))

    # second node
    x,y = x+mx,y+my
    if DEBUG_OPT:
        print("Move to pos ({:d},{:d})".format(x,y))
    contourList.append((x,y)) 

    count = 0


    while(1):
        count += 1
        # time.sleep(1)
        if DEBUG_OPT:
            print("In pos ({:d},{:d}).".format(x,y))
        
        # set the direction to the reverse
        # and rotate by the Counterclockwise(reverse of )
        dirIdx -= 4+1
        if dirIdx < 0:
            dirIdx += 8
        mx,my = dirList[dirIdx]
        
        rotateCount = 0
        if DEBUG_OPT:
            print("Init direction = ({:d},{:d}).".format(mx,my))

        # It's point to black dot, so rotate until it's white
        while img[x+mx,y+my] :
            if DEBUG_OPT:
                print("pos ({:d},{:d}) is Full".format(x+mx,y+my))                
            if rotateCount == 8:
                print("TOO MANY ROTATE!")
                return 0
            rotateCount += 1
            dirIdx -= 1
            if dirIdx < 0:
                dirIdx += 8
            mx,my = dirList[dirIdx]
            if DEBUG_OPT:
                print("Direction = ({:d},{:d}).".format(mx,my))
        # dirIdx -= 1
        # if dirIdx < 0:
        #     dirIdx += 8
        # mx,my = dirList[dirIdx]
        if DEBUG_OPT:
            print("pos ({:d},{:d}) is empty".format(x+mx,y+my))
        x,y = x+mx,y+my
        if DEBUG_OPT:
            print("Move to pos ({:d},{:d})".format(x,y))
        if x == Ox and y == Oy:
            break
        # if abs(x-Ox) <=1 or abs(y-Oy)<=1:
        #     print("Move to pos ({:d},{:d})".format(x,y))
        contourList.append((x,y))   
        if count == 10000:
            break

    return contourList

# dirIdx -= 4
# if dirIdx < 0:
#     dirIdx += 8
# dirIdx += 1
# if dirIdx >= 8:
#     dirIdx -= 8

def getFrame(img):
    l = np.empty_like(img)
    r = np.empty_like(img)
    u = np.empty_like(img)
    d = np.empty_like(img)
    l[:,:-1] = img[:,1:]
    l[:,-1] = img[:,-1]
    d[:-1] = img[1:]
    d[-1] = img[-1]
    r[:,1:] = img[:,:-1]
    r[:,0] = img[:,0]
    u[1:] = img[:-1]
    u[0] = img[0]
    out = np.logical_or(np.logical_or(l,r),np.logical_or(u,d))

    return np.logical_and (np.logical_not(img), out)
    

# def getAllContour(img):
#     data = img.copy()
#     path_leave = 
