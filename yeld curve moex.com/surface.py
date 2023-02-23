from mpl_toolkits.mplot3d import Axes3D 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from analysis import *



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Изменение графика КБД Московской биржи за период')
ax.set_xlabel('Срок до погашения, t')
ax.set_ylabel('Дата')
ax.set_zlabel('Доходность Y(t)')



T, D, Y = getframe(2021, 10, 1, 2022, 2, 20)

df1 = df[dt.datetime(2021, 10, 1): dt.datetime(2022, 2, 20)]
m = list(
    map(
        lambda x: '{}.{}'.format(x.day, x.month),
        df1.index
        )
    )


ax.plot_surface(T, D, Y)

#ax.set_yticks(m)

#ax.set_yticks(days)

plt.show()
