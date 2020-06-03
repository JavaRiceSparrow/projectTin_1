import numpy as np

from utils import *
from imglib import *

class Direction(object):
    #      -X
    #       ^
    #       |
    # -Y<---O---> Y
    #       |
    #       V
    #       X
    # 1 2 3
    # 0 X 4
    # 7 6 5
    
    dirList = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]

    def __init__(self, direIdx = 0):
        self.dir = direIdx
        
        
    def pos(self):
        return self.dirList[self.dir]
    def getDire(self):
        return self.dir
    def rotate(self, direc = True, time = 1):
        # print("[time] {:d}".format(time))
        if time != 1:
            for _ in range(time%8):
                self.rotate(direc = direc)
            return
        if direc:
            self.dir += 1
            if self.dir >= 8:
                self.dir -= 8
        else:
            self.dir -= 1
            if self.dir < 0:
                self.dir += 8
        # print("[time] end.")
    def rotateRev(self):
        self.dir += 4
        if self.dir >= 8:
            self.dir -= 8
        



def getULpos(img):
    if img.sum() == 0:
        return 0
    # print(img.shape)
    sizeX, sizeY = img.shape
    imgt = img.copy()
    sizeS = sizeX+sizeY-1
    URline_bol = np.empty([sizeS],dtype=bool)

    for i in reversed(range(sizeX-1)):
        # print("1:")
        # print(":-1")
        # print(imgt[i+1][:-1].shape)
        imgt[i][1:] = np.logical_or(imgt[i][1:],imgt[i+1][:-1])
        URline_bol[sizeY+i] = imgt[i+1][-1]

    # print(imgt.astype(int))


    URline_bol[:sizeY] = imgt[0]

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

        print('Program Wrong (at getULpos)')
        return 0
    elif pos >= sizeX and pos >= sizeY:
        for i in range(sizeS-pos+1):
            if img[sizeX-1-i,i+pos-sizeX+1]:
                return (sizeX-1-i,i+pos-sizeX+1)


    
    if sizeX > sizeY:
        for i in range(sizeY):
            if img[pos-i][i]:
                return (pos-i,i)
        # pass
    else:
        for i in range(sizeX):
            if img[sizeX-1-i][pos-sizeX+1+i]:
                return (sizeX-1-i,pos-sizeX+1+i)
        # pass
    print("Oops!(at getULpos)")
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
    
def detContour(img, startPoint = 0, errorMsg = []):
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

    if img[Ox,Oy]:
        if DEBUG_OPT:
            print("[Contour] The pos is full!")
        errorMsg.append("[Contour] The pos is full!")
        return 0

    dire = Direction(0)
    x,y = Ox,Oy
    contourList.append((x,y))

    temdire = Direction(0)
    nearList = []
    for i in range(8):
        mx,my = temdire.pos()
        nearList.append(img[x+mx,y+my])
        temdire.rotate(True)


    mx,my = dire.pos()
    rotateCount = 0

    # if not img[x,y]:
    #     errorMsg.append("[Contour] Wrong place in ({:d},{:d})!".format(x,y))
    #     return []
    

    while not nearList[dire.getDire()] :
        if DEBUG_OPT:
            print("Direction = ({:d},{:d}).".format(mx,my))
        if rotateCount == 8:
            if DEBUG_OPT:
                print("[Contour] The pos is inside an empty space!")
            return 0
        rotateCount += 1

        dire.rotate(False)
        mx,my = dire.pos()

    while nearList[dire.getDire()] :
        if DEBUG_OPT:
            print("Direction = ({:d},{:d}).".format(mx,my))
        if rotateCount == 8:
            if DEBUG_OPT:
                print("[Contour] A solely hole in ({:d},{:d})!".format(x,y))
            errorMsg.append("[Contour] A solely hole in ({:d},{:d})!".format(x,y))
            return contourList
        rotateCount += 1

        dire.rotate(False)
        mx,my = dire.pos()

    # mx,my = dirList[dirIdx]
    if DEBUG_OPT:
        print("Start point = ({:d},{:d}).".format(Ox,Oy))
        print("Direction = ({:d},{:d}).".format(mx,my))

    # second node
    mx,my = dire.pos()
    x,y = x+mx,y+my
    if DEBUG_OPT:
        print("Move to pos ({:d},{:d})".format(x,y))
    contourList.append((x,y)) 

    count = 0


    while(1):
        temdire = Direction(0)
        nearList = []
        for _ in range(8):
            mx,my = temdire.pos()
            nearList.append(img[x+mx,y+my])
            temdire.rotate(True)

        # temdire = Direction(0)
        # for _ in range(4):
        #     hit = nearList[temdire.getDire()]
        #     temdire.rotate(True, time=2)
        #     if hit and nearList[temdire.getDire()]:
        #         temdire.rotate(False)
        #         nearList[temdire.getDire()] = True
        #         temdire.rotate(True)





        # print(nearList)
        # # print(contourList)
        # for i in range(x-1,x+2):
        #     for j in range(y-1,y+2):
        #         print(int(img[i][j]),end = ' ')
        #     print()


        count += 1
        # import time
        # time.sleep(0.01)
        if DEBUG_OPT:
            print("In pos ({:d},{:d}).".format(x,y))

        # set the direction to the reverse
        # and rotate by the Counterclockwise(reverse of )
        dire.rotateRev()
        dire.rotate(False)
        mx,my = dire.pos()
        
        rotateCount = 0
        if DEBUG_OPT:
            print("Init direction = ({:d},{:d}).".format(mx,my))

        # It's point to black dot, so rotate until it's white
        # if cross:
        while nearList[dire.getDire()] :
            if DEBUG_OPT:
                mx,my = dire.pos()
                print("pos ({:d},{:d}) is Full".format(x+mx,y+my))                
            if rotateCount == 8:
                print("[Contour] TOO MANY ROTATE!")
                return 0
            rotateCount += 1
            dire.rotate(False)
            if DEBUG_OPT:
                mx,my = dire.pos()
                print("Direction = ({:d},{:d}).".format(mx,my))

        # if dire.getDire()%2 != 0:
        #     dire.rotate(False)
        #     if nearList[dire.getDire()]:
        #         while nearList[dire.getDire()] :
        #             if DEBUG_OPT:
        #                 mx,my = dire.pos()
        #                 print("pos ({:d},{:d}) is Full".format(x+mx,y+my))                
        #             if rotateCount == 8:
        #                 print("[Contour] TOO MANY ROTATE!")
        #                 return 0
        #             rotateCount += 1
        #             dire.rotate(False)
        #             if DEBUG_OPT:
        #                 mx,my = dire.pos()
        #                 print("Direction = ({:d},{:d}).".format(mx,my))
        #     else:
        #         dire.rotate(True)





        if DEBUG_OPT:
            print("pos ({:d},{:d}) is empty".format(x+mx,y+my))
        mx,my = dire.pos()
        x,y = x+mx,y+my
        if DEBUG_OPT:
            print("Move to pos ({:d},{:d})".format(x,y))
        if x == Ox and y == Oy:
            break
        # if abs(x-Ox) <=1 or abs(y-Oy)<=1:
        #     print("Move to pos ({:d},{:d})".format(x,y))
        contourList.append((x,y))   
        if count == 10000:
            print("[Contour] Contour is TOO BIG!")
            # print(contourList)
            break

    return contourList

# dirIdx -= 4
# if dirIdx < 0:
#     dirIdx += 8
# dirIdx += 1
# if dirIdx >= 8:
#     dirIdx -= 8

# from imglib import *
# import color
def getAllContour(img, errorMsg = []):
    DEBUG_OPT = True
    # DEBUG_OPT = False

    data = img.copy()
    path_leave = getFrame(data)

    contours = []
    # i = 0
    

    while(np.sum(path_leave) != 0):
        start = getULpos(path_leave)
        # print(start)
        x,y = start
        # for i in range(x-1,x+2):
        #     for j in range(y-1,y+2):
        #         print(int(img[i][j]),end = ' ')
        #     print()
        # print(np.sum(path_leave))
        # import time
        # time.sleep(1)
        # # TODO: ...
        # if i>10:
        #     sys.exit(0)
        # errorMsg = []
        contour = detContour(data,start, errorMsg=errorMsg)

        # pl1 = arrToImg (path_leave)
        # for pos in contour:
        #     x,y = pos
        #     pl1[x,y] = color.mix(pl1[x,y] , np.array([250,0,0]))
        
        # x,y = start
        # pl1[x,y] = color.mix(pl1[x,y] , np.array([0,250,0]))
        # pl1[x-1,y] = color.mix(pl1[x-1,y] , np.array([0,250,0]))
        # pl1[x+1,y] = color.mix(pl1[x+1,y] , np.array([0,250,0]))
        # pl1[x,y-1] = color.mix(pl1[x,y-1] , np.array([0,250,0]))
        # pl1[x,y+1] = color.mix(pl1[x,y+1] , np.array([0,250,0]))

        # pathList = ["dump/",str(i),".bmp" ]
        # path = "".join(pathList)
        # saveImg(pl1, path)
        # # print(len(contour))

        # if DEBUG_OPT and len(errorMsg) != 0:
        #     print(errorMsg)
        
        for pos in contour:
            x,y = pos
            path_leave[x][y] = False
        contours.append(contour)

        # i += 1

    return contours


