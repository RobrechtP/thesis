import fnmatch
import numpy as np
import math
a = np.array([1,2,3])
b = np.array([5,6,7])
c = np.outer(a,b)


d = np.random.rand(5,4) * 15
d = np.ones((5,3))
d[1][1] = 0.5
print(d)

sum = d.sum(axis=1, keepdims=1)
e = d/sum
print(e)
print(e.sum(1))


for i in range(len(d)):
    d[i] = d[i]/d[i].sum()

print(d)
print(d.sum(1))
print(d.sum(1).sum())

print(a*b)
print(np.sqrt(a*b))

a = np.array([9, 4, 4, 3, 3, 9, 0, 4, 6, 0])
a = np.flip(a)
print(a)

ind = np.argpartition(a, -2)[-2:]
print(ind)
print (np.power(2.3,2))
print (int(np.ceil(0.3)))