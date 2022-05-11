# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:55:12 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

# https://towardsdatascience.com/creating-custom-plotting-functions-with-matplotlib-1f4b8eba6aa1


def plot_circ( R=1, C=(0,0), points=50, ax=None, **plt_kwargs ):
    if ax is None:
        ax = plt.gca()
    angle = np.linspace(0, 2*np.pi, points+1)
    x = C[0] + R*np.cos(angle)
    y = C[1] + R*np.sin(angle)
    ax.plot( x,y, **plt_kwargs )
    ax.axis('equal')

plt.figure()
plot_circ(R=2, C=[1,0], c='k', linestyle='-.', label='1')
plot_circ(C=[0,1], points=5, c=(112/255,48/255,160/255), linestyle='', marker='^', label='2')
plt.legend()
plt.show()