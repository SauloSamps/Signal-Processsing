# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:16:16 2024

@author: Saulo
"""

import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import LorentzianModel
from lmfit import create_params, fit_report, minimize, Parameters
#from modules import 

data = np.loadtxt('example.csv', delimiter=',', skiprows=1)
x = data[:, 0]
y = data[:, 1]

params = create_params(center=5, gamma=1, amplitude=5)
out = minimize(lorentzian_residual, params, method='nelder', args=(x,), kws={'data': y})

#print(fit_report(out))
#print(out.params['center'].stderr)
print(out.params['center'].stderr)