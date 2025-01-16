# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:16:16 2024

@author: Saulo
"""

import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import LorentzianModel
from lmfit import create_params, fit_report, minimize, Parameters
from modules import *



generateCurves(gamma=1, x0=0, xmin=-10, xmax=10, numberOfPoints=100, height=1, noiseRange=10, totalNoiseDatapoints=100, curvesPerNoise=100)
y_amplitude, y_gamma, y_center, fails = runFittingAlg(noiseRange=10, totalNoiseDatapoints=100, curvesPerNoise=100, method='leastsq')

print(fails)
#x_noise = np.linspace(0.0, 1, 100)
#showError(x_noise, y_amplitude, y_center, y_gamma, title='Fit error with LM', xlabel='Noise Level', ylabel='stderr', filename="Error-LM-3.png")