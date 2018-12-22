#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d') # return a Axes3D object
ax.scatter([0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4])
plt.show()
