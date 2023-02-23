def r(p, x):
    return p*x-(0.5*x**2+2*x+6)

S = 0
for i in range(0, 10):
    ri = r(10 + i, 8 + i)
    S += ri
    print('ri = {}, S = {}'.format(ri, S))

    
import numpy as np

X = np.linspace(1, 100, 101, dtype=np.float32)
P = np.linspace(10, 101, 101-10+1, dtype=np.float32)
X, P = np.meshgrid(X, P)

Z = P*X-(0.5*X**2+2*X+6)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, P, Z)   
plt.show()
