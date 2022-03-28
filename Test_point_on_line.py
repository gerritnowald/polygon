# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 15:11:12 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------
# input

P1 = np.array([2,1])
P2 = np.array([4,5])

Q = np.array([3,3])

# -------------------------------------------------------
# function

def isPointOnLine(P1, P2, Q):
    # Is point Q=[x3,y3] on line from P1=[x1,y1] to P2=[x2,y2]
    # https://de.mathworks.com/matlabcentral/answers/351581-points-lying-within-line
    PQ  =  Q - P1   # Line from P1 to Q
    P12 = P2 - P1   # Line from P1 to P2
    L12 = np.sqrt(np.dot(P12,P12))
    N   = P12/L12   # Normal along the line
    
    Dist  = abs(np.cross(N,PQ))     # Norm of distance vector
    Limit = np.spacing(np.max(np.abs([P1, P2, Q])))*10   # Consider rounding errors
    on    = Dist < Limit
    if on:
        L = np.dot(PQ,N)            # Projection of the vector from P1 to Q on the line:
        on = (L>=0.0 and L<=L12)    # Consider end points  
    return on

# -------------------------------------------------------
# test

plt.plot(P1[0],P1[1],"b+")
plt.plot(P2[0],P2[1],"b+")
plt.plot([P1[0],P2[0]],[P1[1],P2[1]],'k')
plt.plot(Q[0],Q[1],"r+")

print(f'Point on line: {isPointOnLine(P1, P2, Q)}')