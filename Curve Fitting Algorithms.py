# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:04:26 2024

@author: Saulo
"""
import numpy as np
import matplotlib.pyplot as plt


def dataset(filename):
    #OPENS THE DATASET
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    return data

def showGraph(x,y):
    # Plot the data and the linear regression curve
    plt.scatter(x, y, s=5, label='Data')
    #plt.plot(x, model.predict(x.reshape(-1, 1)), color='r', label='Linear Regression')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Linear Regression Fit')
    plt.legend()
    plt.show()


def main():
    # Load dataset
    signal = dataset('Dataset/lorentzian_data_2.csv')
    x = signal[:, 0]
    y = signal[:, 1]
    
    #starts the lm algorithm
    
    showGraph(x, y)
    

if __name__ == "__main__":
    main()
