
from libsvm.python.svmutil import *
from libsvm.python.svm import *
import numpy as np
from utils import *
from funlib import *
from svm_model import *

# DEF_ROW = 1
# DEF_COL = 1
DEF_MOMENT = 1
DEF_EROSION = 1
DEF_LIGHT = 1

DEF_PRINT_FEATURE = 0


def toFeature(data):
    '''
    # Return an (25*10) numpy array, 
    # which consist of 5 column mean and 5 row mean.
    # and 7 moment function 
    '''
    dataSize = data.shape[0]
    # features = []
    colDataOri = np.mean(data, axis = 1)
    rowDataOri = np.mean(data, axis = 2)
    col_len = int(ImgSizeX/5)
    row_len = int(ImgSizeY/5)

    colRaw = np.zeros([dataSize,5])
    rowRaw = np.zeros([dataSize,5])
    for i in range(5):
        start , end =  int(i*ImgSizeX/5), int((i+1)*ImgSizeX/5)
        colRaw[:,i] = np.mean(colDataOri[:,start: end] , axis = 1)
        start , end =  int(i*ImgSizeY/5), int((i+1)*ImgSizeY/5)
        rowRaw[:,i] = np.mean(rowDataOri[:,start: end] , axis = 1)
    feature = np.concatenate((colRaw,rowRaw), axis = 1)
   
    return feature


    # print("colData.shape: " +str(colData.shape))
    # print("x.shape: " +str(x.shape))
# def sim(theChar):

def runModel(theChar, quite = True):

    tranTrue, tranForg = loadAllImg((theChar,1), (1,25))
    testTrue, testForg = loadAllImg((theChar,1), (26,25))
    # print("traTrue.shape: " +str(traTrue.shape))

    tran = np.concatenate((tranTrue[0], tranForg[0]), axis=0)
    test = np.concatenate((testTrue[0], testForg[0]), axis=0)
    # print("tran.shape: " +str(tran.shape))
    y = np.concatenate((np.ones(25), -1*np.ones(25)), axis=0)
    x = toFeature(tran)
    yt = np.concatenate((np.ones(25), -1*np.ones(25)), axis=0)
    xt = toFeature(test)
    print(x[15])



    model = svm_model(x,y,xt,yt, quite = True)
    model.analysis()

    
    return model

theChar = 1

if len(sys.argv) > 1:
    # if ()
    if sys.argv[1] == '-t':
        models = []
        for i in range(12):
            theChar = i+1
            models.append(runModel(theChar))

        labels = []
        for i in range(12):
            theChar = i+1
            print("Charactor ", theChar ,":", end = '\t')
            labels.append(models[i].p_label)
            # np.savetxt('label.csv', models[i].p_label, delimiter=',')
            models[i].output(theChar, label = False)
        labels = np.array(labels)
        # np.savetxt('labele.csv', labels, delimiter=',')

        


    elif sys.argv[1] == '-m':
        theChar = int(sys.argv[2])
        model = runModel(theChar)
        np.savetxt('label.csv', model.p_label, delimiter=',')

        # print(model.p_label)
        

        model.output(theChar)
    else:
        print("Incorrect parameter format!")
else :
        print("No parameter!")



def outputImage(model, test, theChar):

    for i in range(len(model.p_label)):
        if model.p_label[i] == 1:
            path = "output/" + str(theChar) + "/" + str(i+1) + "_t.bmp"
        elif model.p_label[i] == -1:
            path = "output/" + str(theChar) + "/" + str(i+1) + "_f.bmp"
        else:
            print("P_label format is incorrect!")

    saveImg(test[i], path) 
# def my_svm(x, y, xt, yt):

#     prob  = svm_problem(y, x)
#     param = svm_parameter()
#     model = svm_train(y, x, '-t 0 -c 4 -b 1')

#     p_label, p_acc, p_val = svm_predict(yt, xt, model)
#     print(p_label)
#     print(type(yt))
#     dectFg = 0
#     hit = 0

#     for i in range(len(p_label)):
#         if p_label[i] == 1:
#             path = "output/" + str(theChar) + "/" + str(i+1) + "_t.bmp"
#         elif p_label[i] == -1:
#             dectFg += 1
#             if yt[i] == -1:
#                 hit += 1
#             path = "output/" + str(theChar) + "/" + str(i+1) + "_f.bmp"
#         else:
#             print("P_label format is incorrect!")

#         saveImg(test[i], path) 


#     precision = hit/ dectFg * 100
#     recall = hit/ len(yt[yt == -1]) * 100

# print ('Precision = ' + str(precision) + '%')
# print ('Recall = ' + str(recall) + '%')

# # fp = open("output/" + str(theChar) + "/result.txt", "w")
# print (p_label, file = open("output/" + str(theChar) + "/result.txt",'w'))
# print ('Accuracy = ' + str(p_acc[0]) + '%', file = open("output/" + str(theChar) + "/result.txt",'a'))
# print ('Precision = ' + str(precision) + '%', file = open("output/" + str(theChar) + "/result.txt",'a'))
# print ('Recall = ' + str(recall) + '%', file = open("output/" + str(theChar) + "/result.txt",'a'))

# fp.close()