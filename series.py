import numpy as np
import matplotlib.pyplot as plt
import math

#Суммирует n первых членов ряда f(n) и выводит график

n = 20
f = lambda x: (3**x+2**x)/6**x

def sum_series(y):
    S = y[0]
    result = [S]
    for i in y[1:]:
        S += i
        result.append(S)
    return result
        

#X = np.arange(1,n, dtype=np.int32)
X = np.linspace(1, n, n)
y = list(map(f, X))
s = sum_series(y)
plt.plot(X, s, 'r')
plt.plot(X, y, 'g')
plt.show()
