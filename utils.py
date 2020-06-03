import numpy as np


def norm(array):
    std = np.std(array)
    mean = np.mean(array)
    if std == 0:
        return (array-mean)
    return (array-mean)/std
def momentFlat(data, a, b):
    '''
    data is a (n*n) 1d array, convert it to a n*n 2d array
    '''
    # print(data.shape)
    n = int(np.sqrt(len(data)))
    # print(n)
    return moment(data.reshape(n,n),a,b)
def moment(data, a, b):
    if type(a) != int or type(b) != int:
        return False
    
    total = np.sum(data)
    x = len(data)    
    y = len(data[0])
    x1 = np.array(range(x))
    xAr = np.transpose(np.array([x1,]*y))
    y1 = np.array(range(y))
    yAr = np.array([y1,]*x)
    # print( xAr)
    # print( yAr)
    m0_x = np.sum(xAr*data)/total
    m0_y = np.sum(yAr*data)/total
    # print( m0_x)
    # print( m0_y)

    arr_x = np.power((xAr- m0_x),a)
    arr_y = np.power((yAr- m0_y),b)
    
    # print (arr_x)
    # print (arr_y)
    # print(arr_x*arr_y*data)
    return np.sum(arr_x*arr_y*data)/total

def erosion(x, printArray = False):
    if np.sum(x) == 0:
        return x

    x_col = np.zeros(x.shape[1]).reshape(1,x.shape[1])
    y_col = np.zeros(x.shape[0]).reshape(x.shape[0],1)
    # print(x_col.shape)
    # print(x[:-1].shape)
    x_l = np.concatenate((x_col,x[:-1]),axis = 0)
    x_r = np.concatenate((x[1:],x_col),axis = 0)
    x_d = np.concatenate((y_col,x[:,:-1]),axis = 1)
    x_u = np.concatenate((x[:,1:],y_col),axis = 1)

    x1 = x * x_l * x_r * x_u * x_d


    if printArray:
        print(x1)
    return x1

def erosion_3(x, printArray = False):
    if np.sum(x) == 0:
        return 0, 0 ,0
    x1 =erosion(x, printArray)
    x2 =erosion(x1, printArray)
    x3 =erosion(x2, printArray)
    sum_x = np.sum(x)

    t1 = np.sum(x1)/sum_x
    t2 = np.sum(x2)/sum_x
    t3 = np.sum(x3)/sum_x


    # if printArray:
    #     print(x1)
    
    return t1,t2,t3


class cirInt(object):

    def __init__(self, data, CirSize):
        if CirSize<0 :
            print("Wrong input!")
            self.size = 0
            return
        self.size = CirSize
        self.data = data%CirSize
    def __add__(self, other): 
        if type(other) == int:
            newObj = cirInt(self.data+other, self.size)
            return newObj
        if type(other) == cirInt:
            newObj = cirInt(self.data+other, self.size)
            return newObj
    def __sub__(self, other): 
        if type(other) == int:
            newObj = cirInt(self.data-other, self.size)
            return newObj
        if type(other) == cirInt:
            newObj = cirInt(self.data-other, self.size)
            return newObj
    def __str__(self): 
        return self.data
    # def __iadd__(self, other):



    
    # def __gt__(self, other): 
    #     print("No '>'!")
    #     return False
    
    # def __lt__(self, other): 
    #     print("No '<'!")
    #     return False
    def __eq__(self, other): 
        if type(other) == int:
            return other%self.size == self.data
        if type(other) == cirInt:
            return other.size == self.size \
            and other.data == self.data
    def __ne__(self, other):
        return not self==other


