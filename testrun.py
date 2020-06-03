import os 
import numpy as np


# from PIL import Image
# try:  
#     img  = Image.open(path)  
# except IOError: 
#     pass

# rawData = np.array(img)
# brightData = rawData[:,:,0]*0.299+ \
# 	rawData[:,:,1]*0.587+rawData[:,:,0]*0.114

# data = 255*(brightData>220)
# data1 = np.expand_dims(data, axis = 2)

# bmpImg =  np.concatenate([data1, data1, data1], axis=2).astype('uint8')

# # print(bmpImg.shape)
# # mp.image.imsave('result.bmp', bmpImg)
# im = Image.fromarray(bmpImg)
# im.save("result1.bmp")
from contour import *
temdire = Direction(0)
nearList = [True,False,True,False, True, False,True,  False]
for i in nearList:
    print(int(i), end = ' ')
print()
for _ in range(4):
    # print(temdire.getDire())
    hit = nearList[temdire.getDire()]
    temdire.rotate(True, time=2)
    if hit and nearList[temdire.getDire()]:
        # print("start")
        temdire.rotate(False)
        nearList[temdire.getDire()] = True
        temdire.rotate(True)
for i in nearList:
    print(int(i), end = ' ')
print()



# from utils import *
# # np.array([[3,4,5],[1,2,3],[9,5,1]])
# a = np.array([[0,1,1,0],[1,1,1,0],[1,1,1,1],[0,1,1,1],[0,1,1,1]])
# print(a)
# t1, a1 =erosion(a,True)
# t2, a2 =erosion(a1,True)
# t3, a3 =erosion(a2,True)
# parameters = [(2,0),(1,1),(0,2),(3,0),(2,1),(1,2),(0,3)]