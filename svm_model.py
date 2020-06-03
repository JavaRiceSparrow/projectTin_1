import sys
from libsvm.python.svmutil import *
from libsvm.python.svm import *
import numpy as np

class svm_model:
    def __init__(self, x, y, xt, yt, quite = False):
        self.prob = None
        self.model = None
        self.x = x
        self.y = y
        self.xt = xt
        self.yt = yt
        self.quite = quite
        
    def analysis(self):

        # self.prob  = svm_problem(self.y, self.x)
        # param = svm_parameter()
        if self.quite:
            self.model = svm_train(self.y, self.x, '-t 0 -c 4 -b 1 -q')
        else:
            self.model = svm_train(self.y, self.x, '-t 0 -c 4 -b 1')

        self.p_label, self.p_acc, self.p_val = svm_predict(self.yt, self.xt, self.model)
        dectFg = 0
        hit = 0
        labelArr = np.array(self.p_label)
        dectArr = (labelArr == -1)
        hitArr = dectArr*(self.yt == -1)
        dectFg = np.sum(dectArr)
        hit = np.sum(hitArr)
        # for i in range(len(self.p_label)):
        #     if self.p_label[i] == -1:
        #         dectFg += 1
        #         if self.yt[i] == -1:
        #             hit += 1

        self.precision = hit/ dectFg * 100
        self.recall = hit/ np.sum(self.yt == -1) * 100

    # def outputImage(self, theChar):

    #     for i in range(len(self.p_label)):
    #         if self.p_label[i] == 1:
    #             path = "output/" + str(theChar) + "/" + str(i+1) + "_t.bmp"
    #         elif p_label[i] == -1:
    #             path = "output/" + str(theChar) + "/" + str(i+1) + "_f.bmp"
    #         else:
    #             print("P_label format is incorrect!")

    #     saveImg(test[i], path) 
    def output(self, theChar, toTxt = False, label = True):
        ch = 0
        if not toTxt:
            if label:
                print (self.p_label)
            if ch:
                print ('Accuracy = {0:.2f}%'.format(self.p_acc[0]), end = "\t")
                print ('Precision = {0:.2f}%'.format(self.precision), end = "\t")
                print ('Recall = {0:.2f}%'.format(self.recall))
            else:
                print ('{0:.2f}%'.format(self.p_acc[0]), end = "\t")
                print ('{0:.2f}%'.format(self.precision), end = "\t")
                print ('{0:.2f}%'.format(self.recall))
            # print()
        else:
            if label:
                print (self.p_label, file = open("output/" + str(theChar) + "/result.txt",'w'))
            print ('Accuracy = {0:.2f}%'.format(self.p_acc[0]), file = open("output/" + str(theChar) + "/result.txt",'a'), end = "\t")
            print ('Precision = {0:.2f}%'.format(self.precision), file = open("output/" + str(theChar) + "/result.txt",'a'), end = "\t")
            print ('Recall = {0:.2f}%'.format(self.recall) , file = open("output/" + str(theChar) + "/result.txt",'a'))
            # print ('Accuracy = ' + str(self.p_acc[0]) + '%', file = open("output/" + str(theChar) + "/result.txt",'a'), end = "\t")
            # print ('Precision = ' + str(self.precision) + '%', file = open("output/" + str(theChar) + "/result.txt",'a'), end = "\t")
            # print ('Recall = ' + str(self.recall) + '%', file = open("output/" + str(theChar) + "/result.txt",'a'))

