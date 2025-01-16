import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import LorentzianModel
from lmfit import create_params, fit_report, minimize, Parameters

def lorentzian(x, x0, gamma, maximum):
    return maximum / (1 + ((x - x0) / gamma)**2)

def lorentzian_residual(params, x, data=None):
    x0 = params['center']
    gamma = params['gamma']
    maximum = params['amplitude']
    
    model = lorentzian(x, x0, gamma, maximum)
    
    if data is None:
        return model
    return model - data

def generateFit(gamma, x0, xmin, xmax, numberOfPoints, height):
    x = np.linspace(xmin, xmax, numberOfPoints)  # Generate x-values
    y = lorentzian(x, x0, gamma, height)  # Calculate y-values
    return x,y

def showFit(x_fit, y_fit, x, y):
    plt.scatter(x, y, label='Data', color='r', s=5)
    plt.plot(x_fit, y_fit, label='Fitted Curve', color='b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise = 0.1')
    plt.legend()
    plt.show()
    plt.clf()

def showData(xData, yData):
    plt.scatter(xData, yData, label='Data Points', color='r', s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise')
    plt.legend()
    plt.show()


data = np.loadtxt('example.csv', delimiter=',', skiprows=1)
x = data[:, 0]
y = data[:, 1]

params = create_params(center=5, gamma=1, amplitude=5)
out = minimize(lorentzian_residual, params, method='nelder', args=(x,), kws={'data': y})

print(fit_report(out))
#print(out.params['center'].stderr)