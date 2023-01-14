# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 05:08:28 2023

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt


Vertices = np.random.rand(3,2)*10


def plot(Vertices, numbers = False, ax = None, **plt_kwargs):
    # plots contour of polygon, optionally with numbers of vertices
    if ax is None:
        ax = plt.gca()
    ax.plot(Vertices[:,0], Vertices[:,1], **plt_kwargs)
    if numbers:
        for i in range(len(Vertices)-1):
            ax.text(Vertices[i,0], Vertices[i,1], str(i) )

plt.close('all')
plt.figure()
plot(Vertices, numbers=True, c='k', marker='o', label='Polygon')
plt.legend()
plt.show()