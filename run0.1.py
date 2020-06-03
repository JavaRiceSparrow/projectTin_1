from libsvm.python.svmutil import *
from libsvm.python.svm import *
import numpy as np
from funlib import *

traTrue, traForg = loadAllImg((1,1), (1,25))
tesTrue, tesForg = loadAllImg((1,1), (26,25))
# tran = 
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# plt.imshow(traTrue[0,14]/255,cmap = 'hot')
# saveImg(traTrue[0,19], "re1.bmp")

# print(traTrue[0,24])

def toFeature(data):
    '''
    Return an (25*10) numpy array, 
    which consist of 5 column mean and 5 row mean.
    '''
    colDataOri = np.mean(data, axis = 1)
    rowDataOri = np.mean(data, axis = 2)
    col_len = int(ImgSizeX/5)
    row_len = int(ImgSizeY/5)
    colData = np.zeros([25,5])
    rowData = np.zeros([25,5])
    for i in range(5):
        start , end =  int(i*ImgSizeX/5), int((i+1)*ImgSizeX/5)
        colData[:,i] = np.mean(colDataOri[:,start: end] , axis = 1)
        start , end =  int(i*ImgSizeY/5), int((i+1)*ImgSizeY/5)
        rowData[:,i] = np.mean(rowDataOri[:,start: end] , axis = 1)

    return np.concatenate((colData, rowData), axis = 1)
    # print("colData.shape: " +str(colData.shape))
    # print("x.shape: " +str(x.shape))

y = np.concatenate((np.ones(25), -1*np.ones(25)), axis=0)

x1, x2 = toFeature(traTrue[0]),  toFeature(traForg[0])
x = np.concatenate((x1,x2), axis=0)
# print("x.shape: " +str(x.shape))


# y, x = [1,-1], [[1,1], [-1,-1]]
# print (type(y))
prob  = svm_problem(y, x)
# print(prob)
# prob
param = svm_parameter()
model = svm_train(y, x, '-t 0 -c 4 -b 1')
# model = svm_train(prob, param)
yt = np.concatenate((np.ones(25), -1*np.ones(25)), axis=0)
xt1, xt2 = toFeature(tesTrue[0]),  toFeature(tesForg[0])
xt = np.concatenate((xt1,xt2), axis=0)
p_label, p_acc, p_val = svm_predict(yt, xt, model)
print(p_label)

for label in p_label:
    if label == 1:
