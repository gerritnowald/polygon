# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 20:18:21 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon


Vertices = np.random.rand(3,2)*10

triangle = polygon(Vertices)

plt.figure()
triangle.plot(numbers=True)
plt.axis('equal')
plt.show()


# function [pos] = center(Pa,Pb,Pc,Type)
# CENTER calculates and shows the orthocenter, circumcenter, barycenter and
# incenter of a triangle, given their vertex's coordinates Pa, Pb and Pc
#
# Example: center([0 0.5 0], [1 0 0], [1 1 3], 'orthocenter')
#
# Made by: Ing. Gustavo Morales, University of Carabobo, Venezuela.
# 09/14/09
#
"""
AB = Pb - Pa 
AC = Pc - Pa 
BC = Pc - Pb # Side vectors

# case 'incenter'# 
uab = AB./norm(AB)
uac = AC./norm(AC)
ubc = BC./norm(BC)
uba = -uab 
L1 = uab + uac
L2 = uba + ubc # directors
P21 = Pb - Pa      
P1 = Pa

# case 'centroid'
L1 = (Pb + Pc)/2 -Pa
L2 = (Pa + Pc)/2 - Pb # directors
P21 = Pb - Pa      
P1 = Pa

# case 'circumcenter'
N = cross(AC,AB)
L1 = cross(AB,N)
L2 = cross(BC,N) # directors
P21 = (Pc - Pa)/2  
P1 = (Pa + Pb)/2

# case 'orthocenter'
N = cross(AC,AB)
L1 = cross(N,BC)
L2 = cross(AC,N) # directors
P21 = Pb - Pa      
P1 = Pa
         
ML = [L1 -L2] # Coefficient Matrix
lambda = ML\P21  # Solving the linear system
pos = P1 + lambda(1)*L1 # Line Equation evaluated at lambda(1)
# X = [Pa(1) Pb(1) Pc(1)] 
# Y = [Pa(2) Pb(2) Pc(2)]
"""