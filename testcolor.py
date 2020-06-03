from contour import *
from endnode import *


from PIL import Image

path1 = '1/1/database/base_1_2_1.bmp'
path2 = '1/4/database/base_1_1_4.bmp'
path3 = '1/7/database/base_1_1_7.bmp'

img1 = getImg(path1)
img2 = getImg(path2)
img3 = getImg(path3)

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
for theChar in range(1,13):
    img = loadAllImg((theChar,1), (1,1), returnType= 0)[0][0]
    edge = getFrame(img)
    contours = getAllContour(img)
    str0 = "tem/origin3_"
    str2 = ".bmp"
    str1 = str(theChar)
    path = str0+str1+str2
    saveImg(img,path)
    # print("There's {:d} contour.".format(len(contours)))
    # for i in range(len(contours)):
    #     print("The {:d} contour has {:d} dots.".format(i,len(contours[i])))
    # print(img.shape)
    # x,y = img.shape
    # saveImg(img1,"tem1.bmp")
    data1 = np.expand_dims(img, axis = 2)
    data = 255*np.concatenate([data1, data1, data1], axis=2).astype('uint8')
    # print('data.shape: '+str(data.shape))
    # image0= Image.fromarray(data, 'RGB')
    # image0.show()
    # print(data.shape)
    # print(data.dtype)
    data0= data.copy()
    data2= data.copy()
    color_blue = np.array([0,255,0])
    for i in range(len(data2)):
        for j in range(len(data2[0])):
            if edge[i,j]:
                data2[i,j] = color_blue

    str0 = "tem/edge3_"
    str2 = ".bmp"
    str1 = str(theChar)
    path = str0+str1+str2
    saveImg(data2,path)
    

    import color
    d = 5
    i = 1
    color_red = np.array([175,50,50])
    color_gray = np.array([150,150,150])
    for contour in contours:
        # print(contour)
        i = 0
        while i<len(contour):
            x,y = contour[i]
            # print(([1, 0, 0]*((5*i)%255)).shape)
            
            # print(d)
            data[x,y] = np.array(color.getHue(i*d))
            # data[x,y] = np.array([0, 0, 0])
            i += 1
        x,y = contour[0]
        # data[x-1,y] = color_red
        # data[x+1,y] = color_red
        # data[x,y-1] = color_red
        # data[x,y+1] = color_red
        data[x,y] = color_gray
        # np.array([255,255,255])

    
    str0 = "tem/contour3_"
    str2 = ".bmp"
    str1 = str(theChar)
    path = str0+str1+str2
    saveImg(data,path)

    nodes = []

    for contour in contours:
        nodeBol = findEndNode(contour,5)
        ctr = np.array(contour)
        for i in ctr[nodeBol]:
            nodes.append(i)
    data3= data.copy()
    for node in nodes:
        x,y = node
        data3[x-1,y] = color_red
        data3[x+1,y] = color_red
        data3[x,y-1] = color_red
        data3[x,y+1] = color_red
        data3[x,y] = np.array([255,255,255])
    
    str0 = "tem/result3_"
    str2 = ".bmp"
    str1 = str(theChar)
    path = str0+str1+str2
    saveImg(data3,path)


    

    

    alldata = np.concatenate((data0, data2, data, data3), axis = 1)

    str0 = "tem/compare3_"
    str2 = ".bmp"
    str1 = str(theChar)
    path = str0+str1+str2
    saveImg(alldata,path)


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