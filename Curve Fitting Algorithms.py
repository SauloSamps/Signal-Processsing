# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:04:26 2024

@author: Saulo
"""
import numpy as np
import matplotlib.pyplot as plt
import levenberg_marquardt as LM
#import example_LM as LM2


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

def levmarAlg(x, y, p_init):
    """
    
    Main function for performing Levenberg-Marquardt curve fitting.

    Parameters
    ----------
    x           : x-values of input data (m x 1), must be 2D array
    y           : y-values of input data (m x 1), must be 2D array
    p_init      : initial guess of parameters values (n x 1), must be 2D array
                  n = 4 in this example

    Returns
    -------
    p       : least-squares optimal estimate of the parameter values
    Chi_sq  : reduced Chi squared error criteria - should be close to 1
    sigma_p : asymptotic standard error of the parameters
    sigma_y : asymptotic standard error of the curve-fit
    corr    : correlation matrix of the parameters
    R_sq    : R-squared cofficient of multiple determination  
    cvg_hst : convergence history (col 1: function calls, col 2: reduced chi-sq,
              col 3 through n: parameter values). Row number corresponds to
              iteration number.

    """
    
    # close all plots
    plt.close('all')
    
    # minimize sum of weighted squared residuals with L-M least squares analysis
    p_fit,Chi_sq,sigma_p,sigma_y,corr,R_sq,cvg_hst = LM.lm(p_init,x,y)
    
    # plot results of L-M least squares analysis
    LM.make_lm_plots(x, y, cvg_hst)
    
    return p_fit,Chi_sq,sigma_p,sigma_y,corr,R_sq,cvg_hst

def main():
    # Load dataset
    signal = dataset('Dataset/lorentzian_data_2.csv')
    x = signal[:, 0]
    y = signal[:, 1]
    
    #starts the lm algorithm
    p_init = np.array([[1.0,1.0,1.0]]).T
    p_fit,Chi_sq,sigma_p,sigma_y,corr,R_sq,cvg_hst = levmarAlg(x,y,p_init)
    
    showGraph(x, y)
    

if __name__ == "__main__":
    main()
