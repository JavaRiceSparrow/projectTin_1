import numpy as np

a = np.array([[1,4],]*7)
print(a.shape)
print(a+1.5)
# a.astype()
b = np.zeros(a.shape)
# b = np.empty_like
print(b-1.2)
# print(np.argmax(a))




# def tem1(i1,arr):
#     arr = np.array([0,2]).copy()
#     # arr[0] = 1

# a1 = np.array([[1,1],[2,3],[0,1]])
# data = a1
# data = np.expand_dims(data, axis = 2)

# data = np.concatenate([data, data, data], axis=2).astype('uint8')
# print(data)
# def mux(a1,a0,b1,b0,s1,s0):
#     c0 = a0*s0 + a0*b0 + (not s1)*(not s0)*b0
#     c1 = ((not s0)*b1 + a1*s0 + s1*(not a1) + (not s0)*b0 + a1*a0)*(not c0)
# value = [True, False]
# for a1 in value:
#     for a0 in value:
#         if a1 and a0:
#             continue
#         for b1 in value:
#             for b0 in value:
#                 if b1 and b0:
#                     continue
#                 for s1 in value:
#                     for s0 in value:
#                         if s1 and s0:
#                             continue
#                         c1,c0 = 



# c0 = a0s0 + a0b0 + s1's0'b0
# c1 = (s0'b1 + a1s0 + s1a1' + s0'b0 + a1a0)*c0' 









# mask = np.array([True,False,True,False])

# '''
# a = np.zeros([5,2])

# b = np.zeros([4,2])
# # a = np.array([[[3,4],]*3,]*4)
# # a[0:2] += np.array([[1,7],]*3)
# # a[1:3] += np.array([[3,-1],]*3)
# a1 = np.transpose(np.array([a,]*4),(1,0,2))
# b1 = np.transpose(np.array([b,]*5),(0,1,2))
# # print(a1.shape)
# # print(b1.shape)
# c = a1-b1
# while c.size != 0:
#     print(c.shape)
#     c = np.delete(c,0,1)
# '''
# a = np.array([[0,2,1],[5,3,4],[7,9,0]])
# print(a)
# result = np.array(np.where(a == np.amax(a))).T
# a = np.delete(a, result[0,0],0)
# a = np.delete(a, result[0,1],1)
# print(result)
# print()
# print(a)
# if type(result == list):
#     for re in result:
#         print(re)
# else:
    # print(result)
# a = np.array([[0,0,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]])
# print(np.delete(a,1,0))
# print(np.delete(a,1,1))
# x = np.sum(a, axis = 0)
# y = np.sum(a, axis = 1)

# print(type(a) == np.ndarray)
# print(x)
# print(y)