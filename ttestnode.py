from contour import *
from endnode import *


from PIL import Image

import color


def getEndNode(img, output = False):
    msg = []
    contours = getAllContour(img, errorMsg = msg)

    data1 = np.expand_dims(img, axis = 2)
    data = 255*np.concatenate([data1, data1, data1], axis=2).astype('uint8')

    data0= data.copy()
  
    nodes = []
    data3= data.copy()
    for contour in contours:
        nodeBol = findEndNode(contour,10)
        ctr = np.array(contour)
        for i in ctr[nodeBol]:
            nodes.append(i)

    for node in nodes:
        x,y = node
        data3[x,y] = np.array([150,150,150])
   
    if output :
        return nodes, data3
    else:
        return nodes

DEF_DEBUG_OPT = True
DEF_DEBUG_OPT = False

# import color

# for theChar in range(1,10):
img_list = []
for theChar in range(1,13):

    if DEF_DEBUG_OPT:
        print("[tn.py]Starting char {:d}...".format(theChar))

    imgArr = loadAllImg((theChar,1), (1,50), returnType= 0)[0]
    imgCount = 0
    outputList = []
    template = loadTemplate(theChar)

    if DEF_DEBUG_OPT:
        print("[tn.py]Getting endnode of char {:d}...".format(theChar))

    tempPointsList, tem_color = getEndNode(template,output=True)
    tempPoints = np.array(tempPointsList).reshape([-1,2])
    tem_color = arrToImg(template)
    colorIdx = 0
    print("Number of endnode of template {:d} is {:d}".format(theChar, len(tempPoints)))
    for point in tempPoints:
        (x,y) = point
        tcolor = np.array(color.getHue(30*colorIdx))
        tem_color[x,y-1:y+2] = tcolor
        tem_color[x-1:x+2,y] = tcolor
        colorIdx += 1

    img_list.append(tem_color)

max_x,max_y = 0,0
img_list2 = []
for img in img_list:
    x,y,_ = img.shape
    max_x = max(max_x,x)
    max_y = max(max_y,y)
# print(max_x, max_y)
for img in img_list:
    x,y,_ = img.shape
    new_arr = np.zeros((max_x,max_y,3))
    new_arr[:x,:y] = img[:,:]
    img_list2.append(new_arr)

# for img in img_list2:
#     print(img.shape)

l1 = img_list2[0:4]
l2 = img_list2[4:8]
l3 = img_list2[8:12]
a1 = np.concatenate(l1,axis = 1)
# print(a1.shape)
a2 = np.concatenate(l2,axis = 1)
a3 = np.concatenate(l3,axis = 1)
Fdata = np.concatenate([a1,a2,a3], axis = 0)

pathList = ["tem/","node/","template_total",".bmp" ]
path = "".join(pathList)
saveImg(Fdata, path)


