import numpy as np

from utils import *
from imglib import *


def findEndNode(Contour,d = 10,threhold = 0.5):

    cSize = len(Contour)
    npCtr = np.array(Contour)

    # print(cSize)

    if (2*d+1) > cSize:
        return npCtr[:0] != npCtr[:0]
        # False matrix
    

    # idx = cirInt(0,cSize)

    # print(npCtr)
    CsubD = np.empty_like(npCtr)
    CaddD = np.empty_like(npCtr)
    # d1 = d % cSize
    # d should not smaller than cSize
    # in this case
    d1 = d
    CsubD[:d1] = npCtr[cSize-d1:]
    CsubD[d1:] = npCtr[:cSize-d1] 
    CaddD[:cSize-d1] = npCtr[d1:]
    CaddD[cSize-d1:] = npCtr[:d1] 
    # print(CsubD)
    # print()
    # print(CaddD)

    # ---c--a--b---> positive
    ab = CaddD - npCtr
    ac = CsubD - npCtr

    dot = np.sum(ab*ac, axis = 1)
    neg = np.logical_not(dot >= np.zeros_like(dot))
    ab_square = np.sum(ab**2, axis = 1)
    ac_square = np.sum(ac**2, axis = 1)
    ab_square[ab_square == 0] = 10000
    ac_square[ac_square == 0] = 10000
    # if (len(ab_square[ab_square == 0])) != 0:
    #     print len(ab_square[ab_square == 0])
    # if (len(ab_square[ab_square == 0])) != 0:
    #     print len(ab_square[ab_square == 0])

    cos_square = dot**2/(ab_square*ac_square)
    
    cos_square[neg] *= -1
    cos_square[cos_square == np.inf] == -1
    cos_square[cos_square == -np.inf] == -1

    def getLocalMax(array, nd, d):
        data = array.copy()
        for _ in range(-nd):
            data1 = np.empty_like(data)
            data1[1:] = data[:-1]
            data1[0] = data[-1]
            data = np.maximum(data, data1)
        for _ in range(d):
            data1 = np.empty_like(data)
            data1[:-1] = data[1:]
            data1[-1] = data[0]
            data = np.maximum(data, data1)

        return np.equal(data, array)

    localMax = getLocalMax(cos_square ,-d,d)
    
    return np.logical_and((cos_square >= threhold), localMax)

    # print(cos_square)

# c1 = [(4,3),(2,5),(1,1),(2,5),(1,1),(2,5),(1,1),(2,5),(1,1),(2,5),(1,1)]
# findEndNode(c1)
def getLocalMax(array, nd, d):
    data = array.copy()
    for _ in range(-nd):
        data1 = np.empty_like(data)
        data1[1:] = data[:-1]
        data1[0] = data[-1]
        data = np.maximum(data, data1)
    for _ in range(d):
        data1 = np.empty_like(data)
        data1[:-1] = data[1:]
        data1[-1] = data[0]
        data = np.maximum(data, data1)

    return np.equal(data, array)

# x = np.array(range(100))/100
# x1 = np.sin(x*np.pi*10)
# x2 = getLocalMax(x1,-5,5)
# for i in range(len(x1)):
#     print("{:.3f},{:b}".format(x1[i],x2[i]), end = ' ')
# print()
# # print()