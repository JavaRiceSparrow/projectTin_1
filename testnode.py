from contour import *
from endnode import *


from PIL import Image

import color



def readTemplate(ft):
    str = ft.readline()
    str_end = len(str)
    nodes = []
    fro = 0
    mid = 0
    end = 0
    for i in range(5):
        while str[fro] != '(':
            fro += 1
            if fro==str_end:
                return nodes
        mid = fro
        while str[mid] != ',':
            mid += 1
        end = mid
        while str[end] != ')':
            end += 1
        

        x = int(str[fro+1:mid])
        y = int(str[mid+1:end])
        nodes.append([x,y])
        if (end == str_end-1):
            break
        fro = end
    return nodes

def nodeNorm(nodes, data):
    nodeArr = np.array(nodes)
    normNodes = np.zeros(nodeArr.shape)
    # nodes.astype(np.float64)
    if len(data.shape) == 2:
        x,y = data.shape
    else:
        # x,y,_ = data.shape
        print("Fuck")

    ax = np.sum(data,axis=1)!=0
    ay = np.sum(data,axis=0)!=0
    # print(ax)
    # print(ay)
    alx = (np.array(range(len(ax)))+1)*ax
    aly = (np.array(range(len(ay)))+1)*ay
    x_max = np.max(alx)-1
    alx[alx==0] = 1000
    x_min = np.min(alx)-1
    y_max = np.max(aly)-1
    aly[aly==0] = 1000
    y_min = np.min(aly)-1
    # print(x_max)
    # print(x_min)
    # print(y_max)
    # print(y_min)
    size = max(x_max-x_min, y_max-y_min)

    # S = np.max(x_max-x_min, y_max-y_min)
    # print(type(nodes[:,0]))
    # print(type((x_max+x_min)/2.0))

    normNodes[:,0] = nodeArr[:,0] -(x_max+x_min)/2.0
    normNodes[:,1] = nodeArr[:,1] -(y_max+y_min)/2.0
    normNodes[:,0] = nodeArr[:,0] *100/size
    normNodes[:,1] = nodeArr[:,1] *100/size
    return normNodes

def getResponseList(nodes, img, tem):
    node_norm = nodeNorm(nodes, img)
    ans = []

    # pointArr = np.array(points)
    tem_pArr = np.array([node_norm,]*len(tem))
    # print(tempPoints.shape)
    if DEF_DEBUG_OPT:
        print("[tn.py]Finding response node of img {:d}...".format(imgCount))
    
    if tempPoints.size != 0:
        tem_pArr = np.transpose(tem_pArr,(1,0,2))
        tem_tArr = np.array([tem,]*len(node_norm))
        # print(tempPoints.shape)
        # points_len*temp_len*2
        # print(tem_tArr.shape)
        d = np.sum((tem_tArr-tem_pArr)**2, axis = 2)
        corresList = []
        while d.size != 0:
            result = np.array(np.where(d == np.amin(d))).T
            # if result.shape[0] == 1:
            pos = result[0]
            ans.append((nodes[pos[0]]))
            d = np.delete(d, pos[0],0)
            d = np.delete(d, pos[1],1)
    # for node in tem:
    #     dist = node_norm-node
    #     dist = np.sum(np.abs(dist),axis = 1)
    #     # dist2 = dist**2
    #     # dist = np.sum(dist2, axis = 1)
    #     idx = np.argmin(dist)
    #     ans.append(nodes[idx])
    return ans


DEF_DEBUG_OPT = True
DEF_DEBUG_OPT = False

# fp = open("tem/temNodes.txt", "w")
# import color
ft = open("template.txt")

# for theChar in range(1,10):
for theChar in range(1,13):
    

    if DEF_DEBUG_OPT:
        print("[tn.py]Starting char {:d}...".format(theChar))

    
    imgCount = 0
    outputList = []
    template = loadTemplate(theChar, temIdx=1)

    if DEF_DEBUG_OPT:
        print("[tn.py]Getting endnode of char {:d}...".format(theChar))

    # tempPointsList,getEndNode(template, threhold_theta=90)
    tempNodeList = readTemplate(ft)

    # tempPoints = np.array(tempPointsList).reshape([-1,2])
    tempPoints = np.array(tempNodeList).reshape([-1,2])
    # for point in tempPoints:
    #     print(point, end = ' ')
    # print()
    tem_color = arrToImg(template)
    colorIdx = 0
    
    for point in tempPoints:
        (x,y) = point
        tcolor = np.array(color.getHue(60*(colorIdx%5)))
        tem_color[x,y-1:y+2] = tcolor
        tem_color[x-1:x+2,y] = tcolor
        colorIdx += 1
        tem_color[colorIdx*5:(colorIdx+1)*5,0:2] = tcolor

    normTemp = nodeNorm(tempPoints, template)
    # for point in normTemp:
    #     print(point, end = ' ')
    # print()


    # pathList = ["tem/","template/","testO_",str(theChar),".bmp" ]
    # path = "".join(pathList)
    # saveImg(tem_color, path)

    # '''
    imgArr = loadAllImg((theChar,1), (1,50), returnType= 0)[0]
    for img in imgArr:
        # print(imgCount)

        if DEF_DEBUG_OPT:
            print("[tn.py]Getting endnode of img {:d}...".format(imgCount))

        points, data = getEndNode(img,output=True)
        outputList.append(data)
        normPoint = getResponseList(points, img, normTemp)
        # print(len(normPoint))
        if (len(normTemp) != len(normPoint)):
            print (len(normTemp))
        colorIdx = 0
        for point in normPoint:
            (x,y) = point
            x = int(x)
            y = int(y)
            # data3[x-1,y] = color_red
            # data3[x+1,y] = color_red
            # data3[x,y-1] = color_red
            # data3[x,y+1] = color_red

            # import color
            tcolor = np.array(color.getHue(60*(colorIdx%5)))
            # tcolor = np.array(color.getHue(50*colorIdx))
            data[x,y-1:y+2] = tcolor
            data[x-1:x+2,y] = tcolor
            colorIdx += 1


        # pointArr = np.array(points)
        # tem_pArr = np.array([pointArr,]*len(tempPoints))
        # # print(tempPoints.shape)
        # if DEF_DEBUG_OPT:
        #     print("[tn.py]Finding response node of img {:d}...".format(imgCount))
        
        # if tempPoints.size != 0:
        #     tem_pArr = np.transpose(tem_pArr,(1,0,2))
        #     tem_tArr = np.array([tempPoints,]*len(pointArr))
        #     # print(tempPoints.shape)
        #     # points_len*temp_len*2
        #     # print(tem_tArr.shape)
        #     d = np.sum((tem_tArr-tem_pArr)**2, axis = 2)
        #     corresList = []
        #     while d.size != 0:
        #         result = np.array(np.where(d == np.amin(d))).T
        #         # if result.shape[0] == 1:
        #         pos = result[0]
        #         corresList.append((pos[1], points[pos[0]]))
        #         d = np.delete(d, pos[0],0)
        #         d = np.delete(d, pos[1],1)

        #     for point in corresList:
        #         colorIdx, (x,y) = point
        #         # data3[x-1,y] = color_red
        #         # data3[x+1,y] = color_red
        #         # data3[x,y-1] = color_red
        #         # data3[x,y+1] = color_red

        #         # import color
        #         tcolor = np.array(color.getHue(30*colorIdx))
        #         # tcolor = np.array(color.getHue(50*colorIdx))
        #         data[x,y-1:y+2] = tcolor
        #         data[x-1:x+2,y] = tcolor


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
    
    tp_x, tp_y, tp_z = tem_color.shape
    
    alldatas.append(np.concatenate((tem_color,np.zeros((5*189-tp_x, tp_y, tp_z))), axis = 0))
    for i in range(10):
        j = 5
        alldatas.append(np.concatenate(tuple(outputList[i*j: (i+1)*j]), axis = 0))

    alldata = np.concatenate(tuple(alldatas), axis = 1)
    # alldata = np.concatenate((arr1,alldata0), axis = 0)
    pathList = ["tem/","nodeTest/","test1_",str(theChar), ".bmp" ]
    path = "".join(pathList)
    saveImg(alldata, path)
    # '''

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