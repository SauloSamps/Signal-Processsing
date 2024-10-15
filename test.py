# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:59:12 2024

@author: Saulo
"""
import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import LorentzianModel

def showData(xData, yData):
    plt.scatter(xData, yData, label='Data Points', color='r', s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise')
    plt.legend()
    plt.show()


data = np.loadtxt('Dataset/0.0/49.csv', delimiter=',', skiprows=1)
x = data[:, 0]
y = data[:, 1]



mod = LorentzianModel()

pars = mod.guess(y, x=x)
out = mod.fit(y, pars, x=x).params
#values = mod.fit(y, pars, x=x).values

print(mod.fit(y, pars, x=x).fit_report(min_correl=0.25))

amplitude_error = out['amplitude'].stderr
gamma_error = out['sigma'].stderr
center_error = out['center'].stderr



showData(x, y)