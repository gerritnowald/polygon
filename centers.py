# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 20:18:21 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon


vert = np.random.rand(3,2)*10

triangle = polygon(vert)

plt.figure()
triangle.plot()
plt.axis('equal')



# first = last vertex
# if not np.isclose(vert[-1,], vert[0,]).all():
#     vert = np.append(vert,[vert[0,]],axis=0)





# https://en.wikipedia.org/wiki/Circumscribed_circle

vertP = vert - vert[0,:]    # coordinate transformation

DP  = np.cross(vertP[:,0],vertP[:,1])[0]
LSQ = np.linalg.norm(vertP, axis=1)**2

UP = np.cross(vertP,LSQ,axis=0)[0,:]/DP/2
UP = UP[::-1]*np.array([-1, 1])     # orthogonal vector

U = UP + vert[0,:]           # coordinate transformation


def plot_circ( R=1, C=(0,0), color='k', points=50 ):
    angle = np.linspace(0, 2*np.pi, points)
    x = C[0] + R*np.cos(angle)
    y = C[1] + R*np.sin(angle)
    plt.plot(x,y, color=color )


plot_circ(np.linalg.norm(UP, ord=2) , U)
plt.show()