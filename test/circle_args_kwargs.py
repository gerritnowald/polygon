# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 13:40:39 2023

@author: ignorama
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_circ(*args, R = 1, C = (0,0), N = 50, **kwargs):
    α = np.linspace(0, 2*np.pi, N+1)
    x = C[0] + R*np.sin(α)
    y = C[1] + R*np.cos(α)
    plt.gca().plot( x, y, *args, **kwargs )
    plt.gca().axis('equal')


plt.close('all')
plt.figure()
plot_circ('k--')
plot_circ('g-', N = 7)
plot_circ('bo', N = 7, markersize = 10)
plt.axis('off')
plt.show()