# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 20:25:02 2020

@author: Parth
"""

import math
from numpy import * #makes for shorter code
from time import time
import matplotlib.pyplot as plt

random.seed(20000)
t0 = time()

S0 = 100
K = 105
T = 1.0
r = 0.05
sigma = 0.2
M = 50
dt = T/M
I = 250000

S = S0 * exp(cumsum((r - 0.5 * sigma ** 2) * dt 
                    + sigma * math.sqrt(dt) 
                    * random.standard_normal((M + 1, I)), axis=0))

S[0] = S0

C0 = math.exp(-r * T) * sum(maximum(S[-1] - K, 0)) / I

tnp2 = time() - t0
print("European Option value %7.3f" % C0)
print("Duration in Seconds %7.3f" % tnp2)

plt.plot(S[:, :10])
plt.grid(True)
plt.xlabel('time step')
plt.ylabel('index level')