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
def getEndNode(img, output = True):
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


# for theChar in range(1,10):
for theChar in range(6,7):
    print(theChar)s
    imgArr = loadAllImg((theChar,1), (1,50), returnType= 0)[0]
    imgCount = 0
    outputList = []
    template = loadTemplate(theChar)
    print("test1")
    tempPointsList, data = getEndNode(template)
    print("get end node")
    tempPoints = np.array(tempPointsList)
    # print(tempPoints)
    

        

