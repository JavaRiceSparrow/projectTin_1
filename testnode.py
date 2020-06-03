from contour import *
from endnode import *


from PIL import Image

img1 = loadTemplate(1, Blight = False)
# path1 = '1/1/database/base_1_2_1.bmp'
# path2 = '1/4/database/base_1_1_4.bmp'
# path3 = '1/7/database/base_1_1_7.bmp'

# img1 = getImg(path1)
# img2 = getImg(path2)
# img3 = getImg(path3)

# x = np.array([[0,0,0,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,1,0,1,0],[0,0,0,0,0]])
# print(x)
# y = getFrame(x)
# print(y.astype(int))


''' {{{Here is the switch!}}}
import color
x,y = 200,200
a = np.zeros((x,y,3))
#######
# r g #
# b y #
#######
# a[0:int(x/2),0:int(y/2)] = np.array(color.getHue(300))
a[0:int(x/2),0:int(y/2)] = [255,0,0]
a[0:int(x/2),int(y/2):] = [0,255,0]
a[int(x/2):,0:int(y/2)] = [0,0,255]
a[int(x/2):,int(y/2):] = [255,255,0]
print(a.shape)
# print(a.dtype)
saveImg(a,"tem/temWin.bmp")
# print(a.dtype)
# '''

""" {{{Here is the switch!}}}
### The xx is for testing detContour()

contour1 = detContour(img1)
# print(contour1)
x,y = img1.shape
# saveImg(img1,"tem1.bmp")
data1 = np.expand_dims(img1, axis = 2)
data = 255*np.concatenate([data1, data1, data1], axis=2).astype('uint8')
# print('data.shape: '+str(data.shape))
# image0= Image.fromarray(data, 'RGB')
# image0.show()
print(data.shape)
# print(data.dtype)
import color
d = 5
i = 1
while i<len(contour1):
    x,y = contour1[i]
    # print(([1, 0, 0]*((5*i)%255)).shape)
    
    # print(d)
    data[x,y] = np.array(color.getHue(i*d))
    # data[x,y] = np.array([0, 0, 0])
    i += 1
x,y = contour1[0]
data[x-1,y] = np.array([255,0,0])
data[x+1,y] = np.array([255,0,0])
data[x,y-1] = np.array([255,0,0])
data[x,y+1] = np.array([255,0,0])
saveImg(data,"tem/test1.bmp")
# print 

#"""
def getEndNode(img, output = False):
    # edge = getFrame(img)
    msg = []
    # print("test2")
    contours = getAllContour(img, errorMsg = msg)
    # print("test3")

    data1 = np.expand_dims(img, axis = 2)
    data = 255*np.concatenate([data1, data1, data1], axis=2).astype('uint8')

    data0= data.copy()
    # data2= data.copy()
    # color_blue = np.array([0,255,0])
    # for i in range(len(data2)):
    #     for j in range(len(data2[0])):
    #         if edge[i,j]:
    #             data2[i,j] = color_blue


    # import color
    # d = 5
    # i = 1
    # # color_red = np.array([175,50,50])
    color_red = np.array([200,0,0])
    # color_yellow = np.array([255,255,0])
    # color_gray = np.array([150,150,150])
    # color_white = np.array([255,255,255])
    # for contour in contours:
    #     i = 0
    #     while i<len(contour):
    #         x,y = contour[i]
    #         data0[x,y] = np.array(color.getHue(i*d))
    #         i += 1
    #     x,y = contour[0]
    #     # data[x-1,y] = color_red
    #     # data[x+1,y] = color_red
    #     # data[x,y-1] = color_red
    #     # data[x,y+1] = color_red
    #     data0[x,y] = color_gray
        # np.array([255,255,255])


    nodes = []
    data3= data.copy()
    for contour in contours:
        nodeBol = findEndNode(contour,10)
        ctr = np.array(contour)
        for i in ctr[nodeBol]:
            nodes.append(i)

    for node in nodes:
        x,y = node
        data3[x,y] = color_red
    # nodes = []
    # for contour in contours:
    #     nodeBol = findEndNode(contour,5)
    #     ctr = np.array(contour)
    #     for i in ctr[nodeBol]:
    #         nodes.append(i)
    # # data3= data.copy()
    # for node in nodes:
    #     x,y = node
    #     # data3[x-1,y] = color_red
    #     # data3[x+1,y] = color_red
    #     # data3[x,y-1] = color_red
    #     # data3[x,y+1] = color_red
    #     if data3[x,y][0] == color_red[0] and data3[x,y][1] == color_red[1]:
    #         data3[x,y] = (color_red+color_yellow)/2
    #     else:
    #         data3[x,y] = color_yellow

    if output :
        return nodes, data3
    else:
        return nodes

DEF_DEBUG_OPT = True
DEF_DEBUG_OPT = False

import color

# for theChar in range(1,10):
for theChar in range(1,10):

    if DEF_DEBUG_OPT:
        print("[tn.py]Starting char {:d}...".format(theChar))

    imgArr = loadAllImg((theChar,1), (1,50), returnType= 0)[0]
    imgCount = 0
    outputList = []
    template = loadTemplate(theChar)

    if DEF_DEBUG_OPT:
        print("[tn.py]Getting endnode of char {:d}...".format(theChar))

    tempPointsList, data = getEndNode(template,output=True)
    tempPoints = np.array(tempPointsList).reshape([-1,2])


    for img in imgArr:
        # print(imgCount)

        if DEF_DEBUG_OPT:
            print("[tn.py]Getting endnode of img {:d}...".format(imgCount))

        points, data = getEndNode(img,output=True)
        outputList.append(data)
        pointArr = np.array(points)
        tem_pArr = np.array([pointArr,]*len(tempPoints))
        # print(tempPoints.shape)
        if DEF_DEBUG_OPT:
            print("[tn.py]Finding response node of img {:d}...".format(imgCount))
        
        if tempPoints.size != 0:
            tem_pArr = np.transpose(tem_pArr,(1,0,2))
            tem_tArr = np.array([tempPoints,]*len(pointArr))
            # print(tempPoints.shape)
            # points_len*temp_len*2
            # print(tem_tArr.shape)
            d = np.sum((tem_tArr-tem_pArr)**2, axis = 2)
            corresList = []
            while d.size != 0:
                result = np.array(np.where(d == np.amin(d))).T
                # if result.shape[0] == 1:
                pos = result[0]
                corresList.append((pos[1], points[pos[0]]))
                d = np.delete(d, pos[0],0)
                d = np.delete(d, pos[1],1)

            for point in corresList:
                colorIdx, (x,y) = point
                # data3[x-1,y] = color_red
                # data3[x+1,y] = color_red
                # data3[x,y-1] = color_red
                # data3[x,y+1] = color_red

                # import color
                data[x,y] = np.array(color.getHue(20+50*colorIdx))


        outputList.append(data)
        if DEF_DEBUG_OPT:
            print("[tn.py]Finish of img {:d}...".format(imgCount))


        

        # pathList = ["tem/","node/","result",str(theChar), \
        # "_",str(imgCount),".bmp" ]
        # path = "".join(pathList)
        # saveImg(data3,path)
        imgCount += 1

    # print(template.shape)

    # for op in outputList:


    # ^  <------------->
    # |  <------------->
    # t  <------------->
    # |  <------------->
    # V  <------------->
    
    alldatas = []
    tem_color = arrToImg(template)
    tp_x, tp_y, tp_z = tem_color.shape
    
    alldatas.append(np.concatenate((tem_color,np.zeros((5*189-tp_x, tp_y, tp_z))), axis = 0))
    for i in range(10):
        j = 5
        alldatas.append(np.concatenate(tuple(outputList[i*j: (i+1)*j]), axis = 0))

    alldata = np.concatenate(tuple(alldatas), axis = 1)
    # alldata = np.concatenate((arr1,alldata0), axis = 0)
    pathList = ["tem/","node/","result",str(theChar), \
    "_","total",".bmp" ]
    path = "".join(pathList)
    saveImg(alldata, path)
    i += 1    
# i = 1
# for op in outputList:
    
#     pathList = ["tem/","node/","result",str(i), \
#     "_","total",".bmp" ]
#     path = "".join(pathList)
#     saveImg(op, path)
#     i += 1    
        
    # alldatas = []
    # for i in range(10):
    #     j = 5
    #     alldatas.append(np.concatenate(tuple(outputList[i*j: (i+1)*j]), axis = 0))

    # alldata = np.concatenate(tuple(alldatas), axis = 1)

    # pathList = ["tem/","node/","result",str(theChar), \
    # "_","total",".bmp" ]
    # path = "".join(pathList)
    # saveImg(data3,path)
    # saveImg(alldata,path)


""" {{{Here is the switch!}}}
### Testing getAllContour()
contours = getAllContour(img3)
print("There's {:d} contour.".format(len(contours)))
for i in range(len(contours)):
    print("The {:d} contour has {:d} dots.".format(i,len(contours[i])))
    
x,y = img3.shape
# saveImg(img1,"tem1.bmp")
data1 = np.expand_dims(img3, axis = 2)
data = 255*np.concatenate([data1, data1, data1], axis=2).astype('uint8')
# print('data.shape: '+str(data.shape))
# image0= Image.fromarray(data, 'RGB')
# image0.show()
# print(data.shape)
# print(data.dtype)

import color
d = 5
i = 1
for contour in contours:
    i = 0
    while i<len(contour):
        x,y = contour[i]
        # print(([1, 0, 0]*((5*i)%255)).shape)
        
        # print(d)
        data[x,y] = np.array(color.getHue(i*d))
        # data[x,y] = np.array([0, 0, 0])
        i += 1
    x,y = contour[0]
    data[x-1,y] = np.array([255,0,0])
    data[x+1,y] = np.array([255,0,0])
    data[x,y-1] = np.array([255,0,0])
    data[x,y+1] = np.array([255,0,0])
    data[x,y] = np.array([255,255,255])
saveImg(data,"tem/test2_3.bmp")
# print 
#"""