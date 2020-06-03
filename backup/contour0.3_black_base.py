import numpy as np

from utils import *
from imglib import *


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
        if URline_bol[i] !=0:
            pos = i
            break
    # print (URline_bol.astype(int).sum())
    # print ("Pos = {:d}".format(pos))
    if pos == sizeS:
        print("It's empty!")
        return 0,0
    if pos < sizeY and pos < sizeX: 
        for i in range(pos+1):
            if img[pos-i][i]:
                return (pos-i,i)

        print('Wrong')
        return 0
    elif pos >= sizeX and pos >= sizeY:
        for i in range(sizeS-pos+1):
            if img[sizeX-1-i,i+pos-sizeX+1]:
                return (sizeX-1-i,i+pos-sizeX+1)


    else:
        print("Oops!")
        return 0

def getFrame(img,neg = False):
    if not neg:
        img_f = img
    else:
        img_f = np.logical_not(img)
    l = np.empty_like(img_f)
    r = np.empty_like(img_f)
    u = np.empty_like(img_f)
    d = np.empty_like(img_f)
    l[:,:-1] = img_f[:,1:]
    l[:,-1] = img_f[:,-1]
    d[:-1] = img_f[1:]
    d[-1] = img_f[-1]
    r[:,1:] = img_f[:,:-1]
    r[:,0] = img_f[:,0]
    u[1:] = img_f[:-1]
    u[0] = img_f[0]
    out = np.logical_or(np.logical_or(l,r),np.logical_or(u,d))

    return np.logical_and (np.logical_not(img_f), out)
    
def detContour(img, startPoint = 0):
    '''
    new version, contour in white(empty) space
    '''

    DEBUG_OPT = True
    DEBUG_OPT = False
    if startPoint == 0:
        Ox,Oy = getULpos(getFrame(img))
        # Oy -= 1
    else:
        Ox,Oy = startPoint
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
    dirIdx = 0
    x,y = Ox,Oy
    contourList.append((x,y))
    mx,my = dirList[dirIdx]
    rotateCount = 0
    

    while not img[x+mx,y+my] :
        if DEBUG_OPT:
            print("Direction = ({:d},{:d}).".format(mx,my))
            if rotateCount == 8:
                print("The pos is inside an empty space!")
                return 0
        rotateCount += 1

        dirIdx -= 1
        if dirIdx < 0:
            dirIdx += 8

        
        mx,my = dirList[dirIdx]

    while img[x+mx,y+my] :
        if DEBUG_OPT:
            print("Direction = ({:d},{:d}).".format(mx,my))
        if rotateCount == 8:
            if DEBUG_OPT:
                print("A solely hole!")
                return contourList
        rotateCount += 1

        dirIdx -= 1
        if dirIdx < 0:
            dirIdx += 8
        mx,my = dirList[dirIdx]

    # mx,my = dirList[dirIdx]
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


def getAllContour(img):
    data = img.copy()
    path_leave = getFrame(data)

    contours = []

    while(np.sum(path_leave) != 0):
        start = getULpos(path_leave)
        # TODO: ...
        contour = detContour(data,start)
        for pos in contour:
            x,y = pos
            path_leave[x][y] = False
        contours.append(contour)

    return contours


