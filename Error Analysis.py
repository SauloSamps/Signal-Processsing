# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:37:17 2024

@author: Saulo
"""
import numpy as np
import os
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
    

def saveData(xData, yData, name):
    # Save (x, y) data to a CSV file
    data = np.column_stack((xData, yData))
    np.savetxt(name, data, delimiter=',', fmt='%.5f,%.5f', header='x,y', comments='')

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
    plt.savefig("Report 2/Amplitude MSE.png", dpi=300, bbox_inches='tight')
    plt.clf()
    
    
    plt.plot(x, group_mse_gamma, label='Gamma', color='b')
    plt.xlabel('Noise Level')
    plt.ylabel('Gamma MSE')
    plt.title('Gamma MSE by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 2/Gamma MSE.png", dpi=300, bbox_inches='tight')
    plt.clf()
    
    plt.plot(x, group_mse_center, label='Center', color='g')
    plt.xlabel('Noise Level')
    plt.ylabel('Center MSE')
    plt.title('Center MSE by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 2/Center MSE.png", dpi=300, bbox_inches='tight')
    plt.clf()
    

def showError(x, y_amplitude, y_center, y_gamma, y_height):
    plt.scatter(x, y_amplitude, label='Amplitude', color='r', s=5)
    plt.scatter(x, y_center, label='Center', color='g', s=5)
    plt.scatter(x, y_gamma, label='Gamma', color='b', s=5)
    plt.scatter(x, y_height, label='Height', color='black', s=5)
    plt.xlabel('Noise Level')
    plt.ylabel('Error')
    plt.title('Fit Error by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 2/Error.png", dpi=300, bbox_inches='tight')
    plt.clf()

def showErrorSeparate(x, y_value, name, color):
    plt.scatter(x, y_value, label=name, color=color, s=5)
    plt.xlabel('Noise Level')
    plt.ylabel('Error')
    plt.title('Fit Error by Noise')
    plt.legend()
    #plt.show()
    plt.savefig("Report 2/" + name + "Error.png", dpi=300, bbox_inches='tight')
    plt.clf()
    

def showData(xData, yData, i):
    plt.scatter(xData, yData, label='Data Points', color='r', s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise = ' + str(i/100))
    plt.legend()
    #plt.show()
    plt.savefig("Report 2/Curves/" + str(i/100) + ".png", dpi=300, bbox_inches='tight')
    plt.clf()

def showFit(x_fit, y_fit, x, y, i):
    plt.scatter(x, y, label='Data', color='r', s=5)
    plt.plot(x_fit, y_fit, label='Fitted Curve', color='b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise = ' + str(i/100))
    plt.legend()
    #plt.show()
    plt.savefig("Report 2/Curves AND fit/" + str(i/100) + ".png", dpi=300, bbox_inches='tight')
    plt.clf()
    
def runFittingAlg():
    y_amplitude = []
    y_gamma = []
    y_center = []
    y_height = []
    
    for i in range(0,40):
        
        amplitude_error_mean = 0
        gamma_error_mean = 0
        center_error_mean = 0
        height_error_mean = 0
            
        if (i%10 == 0):
            print("Progress: " + str(i) + "%")
        
        for j in range(0,100):
            signal = dataset("Dataset/" + str(i/100) + "/" + str(j) + ".csv")
            x = signal[:, 0]
            y = signal[:, 1]
            
            mod = LorentzianModel()
            
            pars = mod.guess(y, x=x)
            out = mod.fit(y, pars, x=x).params
            #values = mod.fit(y, pars, x=x).values
            
            amplitude_error = out['amplitude'].stderr
            gamma_error = out['sigma'].stderr
            center_error = out['center'].stderr
            height_error = out['height'].stderr
            
            amplitude_error_mean += amplitude_error
            gamma_error_mean += gamma_error
            center_error_mean += center_error
            height_error_mean += height_error
            
            """
            if (j%500 == 0 and j!=0):
                x_fit,y_fit = generateFit(values['sigma'], values['center'], -10, 10, 100, values['height'])
                showFit(x_fit, y_fit, x, y, i)
                showData(x,y,i)
            """
            
            
        amplitude_error_mean = amplitude_error_mean/100
        gamma_error_mean = gamma_error_mean/100
        center_error_mean = center_error_mean/100
        height_error_mean = height_error_mean/100
        
        amplitude_error_mean = amplitude_error_mean/np.pi
        
        
        y_amplitude.append(np.around(amplitude_error_mean, decimals=5))
        y_gamma.append(np.around(gamma_error_mean, decimals=5))
        y_center.append(np.around(center_error_mean, decimals=5))
        y_height.append(np.around(height_error_mean, decimals=5))
        
        
        
        
    return y_amplitude, y_gamma, y_center, y_height

def main():
    
    try:
        os.mkdir("Report 2/")
        #os.mkdir("Report 2/Curves AND fit/")
        #os.mkdir("Report 2/Curves/")
    except:
        print("Directories already exist")
    
    x_noise = np.linspace(0.0, 0.40, 40)
    
    y_amplitude, y_gamma, y_center,y_height = runFittingAlg()
    
    #mse_amplitude, mse_gamma, mse_center = calcMSE(y_amplitude, y_gamma, y_center)
    #showMSE(mse_amplitude, mse_gamma, mse_center)
    
    #Generateas error graph with all variables
    showError(x_noise, y_amplitude, y_center, y_gamma, y_height)
    
    #Saves raw error Data
    saveData(x_noise, y_amplitude, "Amplitude Error.csv")
    saveData(x_noise, y_center, "Center Error.csv")
    saveData(x_noise, y_gamma, "Gamma Error.csv")
    saveData(x_noise, y_height, "Height Error.csv")
    
    #Generate Error Graphs separately
    showErrorSeparate(x_noise, y_amplitude, "Amplitude", 'r')
    showErrorSeparate(x_noise, y_center, "Center", 'g')
    showErrorSeparate(x_noise, y_gamma, "Gamma", 'b')
    showErrorSeparate(x_noise, y_height, "Height", 'black')
    
    
    
    
    
if __name__ == "__main__":        
    main()