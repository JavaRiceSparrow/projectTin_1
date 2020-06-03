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
    
    # elif pos >= sizeY and pos >= sizeX:
    #     for i in range(sizeS -pos +1):
    #         if img[pos-i][i]:
    #             return (pos-i,i)

    #     print('Wrong')
    #     return 0
    
    # else:
    #     for i in range(pos-sizeX,sizeY):
    #         if img[pos-i][i]:
    #             return (pos-i,i)

    #     print('Wrong')
    #     return 0
    else:
        print("Oops!")

def detContour(img):
    '''
    new version, contour in white(empty) space
    '''

    DEBUG_OPT = True
    # DEBUG_OPT = False

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
    count = 0

    

    # if DEBUG_OPT:
    #     print("{:d},{:d}".format(x,y))
    #     print(img[x-1:x+2,y-1:y+2].astype(int))

    # No need, because the only black near dot is at (1,1)
    # # choose first direction
    # # Find out the direcion of the last white space

    # while not img[x+mx,y+my] :
    #     if DEBUG_OPT:
    #         print("Direction = ({:d},{:d}).".format(mx,my))
    #         if count == 8:
    #             print("The pos is inside an empty space!")
    #             return 0
    #     count += 1

    #     dirIdx -= 1
    #     if dirIdx < 0:
    #         dirIdx += 8

        
    #     mx,my = dirList[dirIdx]

    # while img[x+mx,y+my] :
    #     if DEBUG_OPT:
    #         print("Direction = ({:d},{:d}).".format(mx,my))
    #     if count == 8:
    #         if DEBUG_OPT:
    #             print("A solely hole!")
    #             return contourList
    #     count += 1

    #     dirIdx -= 1
    #     if dirIdx < 0:
    #         dirIdx += 8
    #     mx,my = dirList[dirIdx]
    
    
    # dirIdx -= 1
    # if dirIdx <0:
    #     dirIdx += 8
    mx,my = dirList[dirIdx]
    if DEBUG_OPT:
        print("Start point = ({:d},{:d}).".format(Ox,Oy))
        print("Direction = ({:d},{:d}).".format(mx,my))

    # second node
    x,y = x+mx,y+my
    if DEBUG_OPT:
        print("Move to pos ({:d},{:d})".format(x,y))
    contourList.append((x,y)) 


    while(1):
        # if DEBUG_OPT:
        #     print("{:d},{:d}".format(x,y))
        #     print(img[x-1:x+2,y-1:y+2].astype(int))
        if DEBUG_OPT:
            print("In pos ({:d},{:d}).".format(x,y))
        
        # set the direction to the reverse
        # and rotate by the counterclockwise(reverse of )
        dirIdx -= 4+1
        if dirIdx < 0:
            dirIdx += 8
        mx,my = dirList[dirIdx]
        
        if DEBUG_OPT:
            count = 0
            print("Direction = ({:d},{:d}).".format(mx,my))

        # It's point to black dot, so rotate until it's white
        while img[x+mx,y+my] :
            if DEBUG_OPT:
                print("pos ({:d},{:d}) is empty".format(x+mx,y+my))                
            if count == 8:
                print("TOO MANY ROTATE!")
                return 0
            count += 1
            dirIdx -= 1
            if dirIdx < 0:
                dirIdx += 8
            mx,my = dirList[dirIdx]
            if DEBUG_OPT:
                print("Direction = ({:d},{:d}).".format(mx,my))
        
        if DEBUG_OPT:
            print("pos ({:d},{:d}) is full".format(x+mx,y+my))
        x,y = x+mx,y+my
        if DEBUG_OPT:
            print("Move to pos ({:d},{:d})".format(x,y))
        if x == Ox and y == Oy:
            break
        contourList.append((x,y))   

        # if ()
    return contourList
    


# def detContour(img):

#     DEBUG_OPT = True
#     # DEBUG_OPT = False

#     Ox,Oy = getULpos(img)
#     sizeX,sizeY = img.shape
#     contourList = []

#     #      -X
#     #       ^
#     #       |
#     # -Y<---O---> Y
#     #       |
#     #       V
#     #       X

    
#     dirList = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
#     dirIdx = 0
#     x,y = Ox,Oy
#     contourList.append((x,y))
#     mx,my = dirList[dirIdx]
#     # choose first direction
#     if DEBUG_OPT:
#         count = 0
#         print("{:d},{:d}".format(x,y))
#         print(img[x-1:x+2,y-1:y+2].astype(int))
#         # print("In pos ({:d},{:d}).".format(x,y))
#     # if DEBUG_OPT:
#     while img[x+mx,y+my] :
#         if DEBUG_OPT:
#             print("Direction = ({:d},{:d}).".format(mx,my))
#             count += 1
#             if count == 8:
#                 print("TOO MANY ROTATE!")
#         dirIdx += 1
#         if (dirIdx > 7):
#             dirIdx = 0
#         mx,my = dirList[dirIdx]
#     while not img[x+mx,y+my] :
#         if DEBUG_OPT:
#             print("Direction = ({:d},{:d}).".format(mx,my))
#             count += 1
#             if count == 8:
#                 print("TOO MANY ROTATE!")
#         dirIdx += 1
#         if (dirIdx > 7):
#             dirIdx = 0
#         mx,my = dirList[dirIdx]
#     if DEBUG_OPT:
#         print("Direction = ({:d},{:d}).".format(mx,my))


#     while(1):
#         if DEBUG_OPT:
#             print("In pos ({:d},{:d}).".format(x,y))
#         dirIdx += (4+1)
#         if (dirIdx > 7):
#             dirIdx -= 8
#         mx,my = dirList[dirIdx]
        
#         if DEBUG_OPT:
#             count = 0
#             print("Direction = ({:d},{:d}).".format(mx,my))

#         while not img[x+mx,y+my] :
#             if DEBUG_OPT:
#                 print("pos ({:d},{:d}) is empty".format(x+mx,y+my))
#                 count += 1
#                 if count == 8:
#                     print("TOO MANY ROTATE!")
#             dirIdx += 1
#             if (dirIdx > 7):
#                 dirIdx = 0
#             mx,my = dirList[dirIdx]
#             if DEBUG_OPT:
#                 print("Direction = ({:d},{:d}).".format(mx,my))
        
#         if DEBUG_OPT:
#             print("pos ({:d},{:d}) is full".format(x+mx,y+my))
#         x,y = x+mx,y+my
#         if DEBUG_OPT:
#             print("Move to pos ({:d},{:d})".format(x,y))
#         if x == Ox and y == Oy:
#             break
#         contourList.append((x,y))   

#         # if ()
#     return contourList
    


