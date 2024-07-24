# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:37:17 2024

@author: Saulo
"""
import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import LorentzianModel

def lorentzian(x, x0, gamma, maximum):
    #x0 is the center for the curve
    #gamma is the width of the curve
    #maximum is the amplitude
    
    #maximum = maximum * np.pi
    #return (maximum/np.pi) * (gamma / ((x - x0)**2 + gamma**2))
    
    #return maximum * (gamma / ((x - x0)**2 + gamma**2))
    #return maximum / (np.pi * gamma**2 + (x - x0)**2)
    
    return maximum / (1 + ((x - x0) / gamma)**2)


def generateFit(gamma, x0, xmin, xmax, numberOfPoints, height):
    """
    --------------------------------------------------------------
    GENERATES A RANDOM DATASET IN THE SHAPE OF A LORENTZIAN CURVE
    --------------------------------------------------------------
    
    gamma -> width of the lorentzian curve
    x0 -> center of the lorentzian curve
    xmin -> lowest x value
    xmax -> max x value
    numberOfPoints -> total number of data points
    height -> max value of y
    """
    
    x = np.linspace(xmin, xmax, numberOfPoints)  # Generate x-values
    
    y = lorentzian(x, x0, gamma, height)  # Calculate y-values
    return x,y

def dataset(filename):
    #OPENS THE DATASET
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    return data
    

def calcMSE(y_amplitude, y_gamma, y_center):
    group_mse_amplitude = []
    group_mse_center = []
    group_mse_gamma = []
    for i in range (0, 10):
        group_amplitude = y_amplitude[(i*10):((i*10)+9)]
        group_center = y_center[(i*10):((i*10)+9)]
        group_gamma = y_gamma[(i*10):((i*10)+9)]
        
        mse_amplitude = (sum(group_amplitude)**2)/len(group_amplitude)
        mse_center = (sum(group_center)**2)/len(group_center)
        mse_gamma = (sum(group_gamma)**2)/len(group_gamma)
        
        group_mse_amplitude.append(mse_amplitude)
        group_mse_center.append(mse_center)
        group_mse_gamma.append(mse_gamma)
        
    return group_mse_amplitude, group_mse_gamma, group_mse_center

def showMSE(group_mse_amplitude, group_mse_gamma, group_mse_center):
    x = [0.045, 0.145, 0.245, 0.345, 0.445, 0.545, 0.645, 0.745, 0.845, 0.945]
    
    plt.plot(x, group_mse_amplitude, label='Amplitude', color='r')
    plt.xlabel('Noise Level')
    plt.ylabel('Amplitude MSE')
    plt.title('Amplitude MSE by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 1/Amplitude MSE.png", dpi=300, bbox_inches='tight')
    plt.clf()
    
    
    plt.plot(x, group_mse_gamma, label='Gamma', color='b')
    plt.xlabel('Noise Level')
    plt.ylabel('Gamma MSE')
    plt.title('Gamma MSE by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 1/Gamma MSE.png", dpi=300, bbox_inches='tight')
    plt.clf()
    
    plt.plot(x, group_mse_center, label='Center', color='g')
    plt.xlabel('Noise Level')
    plt.ylabel('Center MSE')
    plt.title('Center MSE by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 1/Center MSE.png", dpi=300, bbox_inches='tight')
    plt.clf()
    

def showError(x, y_amplitude, y_center, y_gamma):
    plt.scatter(x, y_amplitude, label='Amplitude', color='r', s=5)
    plt.scatter(x, y_center, label='Center', color='g', s=5)
    plt.scatter(x, y_gamma, label='Gamma', color='b', s=5)
    plt.xlabel('Noise Level')
    plt.ylabel('Error')
    plt.title('Fit Error by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 1/Error.png", dpi=300, bbox_inches='tight')
    plt.clf()
    

def showData(xData, yData, i):
    plt.scatter(xData, yData, label='Data Points', color='r', s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise = ' + str(i/100))
    plt.legend()
    #plt.show()
    plt.savefig("Report 1/Curves/" + str(i/100) + ".png", dpi=300, bbox_inches='tight')
    plt.clf()

def showFit(x_fit, y_fit, x, y, i):
    plt.scatter(x, y, label='Data', color='r', s=5)
    plt.plot(x_fit, y_fit, label='Fitted Curve', color='b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise = ' + str(i/100))
    plt.legend()
    #plt.show()
    plt.savefig("Report 1/Curves AND fit/" + str(i/100) + ".png", dpi=300, bbox_inches='tight')
    plt.clf()
    
def runFittingAlg():
    y_amplitude = []
    y_gamma = []
    y_center = []
    for i in range(0,100):
        signal = dataset("Dataset/" + str(i/100) + ".csv")
        x = signal[:, 0]
        y = signal[:, 1]
        
        mod = LorentzianModel()
        
        pars = mod.guess(y, x=x)
        out = mod.fit(y, pars, x=x)
        values = out.values
        
        
        y_amplitude.append(np.around(abs(values['height'] - 10), decimals=5))
        y_gamma.append(np.around(abs(values['sigma'] - 1), decimals=5))
        y_center.append(np.around(abs(values['center'] - 0), decimals=5))
        
        showData(x,y,i)
        
        x_fit,y_fit = generateFit(values['sigma'], values['center'], -10, 10, 100, values['height'])
        showFit(x_fit, y_fit, x, y, i)
        
    return y_amplitude, y_gamma, y_center

def main():
    x_noise = np.linspace(0.0, 0.99, 100)
    
    y_amplitude, y_gamma, y_center = runFittingAlg()
    
    mse_amplitude, mse_gamma, mse_center = calcMSE(y_amplitude, y_gamma, y_center)
    showMSE(mse_amplitude, mse_gamma, mse_center)
    
    showError(x_noise, y_amplitude, y_center, y_gamma)
    
    
    
    
    
if __name__ == "__main__":        
    main()