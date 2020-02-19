# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 21:37:06 2020

@author: Parth
"""

S0 = 100
K = 105
T = 1.0
r = 0.05
sigma = 0.2

import numpy

I = 100000

z = numpy.random.standard_normal(I)
ST = S0*numpy.exp((r - 0.5*sigma**2)*T+sigma*numpy.sqrt(T)*z)
hT = numpy.maximum(ST-K,0)
C0=numpy.exp(-r*T)*sum(hT)/I

print("Value of the European Call Option %5.3f" % C0)

