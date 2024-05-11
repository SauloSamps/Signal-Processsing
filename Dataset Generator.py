import numpy as np
from random import uniform
import matplotlib.pyplot as plt

def lorentzian(x, x0, gamma, maximum):
    #x0 is the center for the curve
    #gamma is the width of the curve
    #maximum is the amplitude
    
    #maximum = maximum * np.pi
    #return (maximum/np.pi) * (gamma / ((x - x0)**2 + gamma**2))
    maximum = maximum*gamma
    return maximum * (gamma / ((x - x0)**2 + gamma**2))

def generateData(gamma, x0, xmin, xmax, numberOfPoints, amplitude):
    """
    --------------------------------------------------------------
    GENERATES A RANDOM DATASET IN THE SHAPE OF A LORENTZIAN CURVE
    --------------------------------------------------------------
    
    gamma -> width of the lorentzian curve
    x0 -> center of the lorentzian curve
    xmin -> lowest x value
    xmax -> max x value
    numberOfPoints -> total number of data points
    amplitude -> max value of y
    """
    
    x = np.linspace(xmin, xmax, numberOfPoints)  # Generate x-values
    
    y = lorentzian(x, x0, gamma, amplitude)  # Calculate y-values
    return x,y

def addWhiteNoiseRandom(xData, yData, factor):
    y_noisy = yData + np.random.normal(0, factor, len(xData))
    return y_noisy

def saveData(xData, yData, name):
    # Save (x, y) data to a CSV file
    data = np.column_stack((xData, yData))
    np.savetxt(name, data, delimiter=',', fmt='%.5f,%.5f', header='x,y', comments='')
    
def showData(xData, yData):
    plt.scatter(xData, yData, label='Data Points', color='r', s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise')
    plt.legend()
    plt.show()

def main():
    datasetSize = 1000
    
    for i in range (datasetSize):
        gamma = np.around(uniform(1.0, 3.0), decimals=3)
        center = np.around(uniform(-9.0, 9.0), decimals=3)
        amplitude = np.around(uniform(4.0, 10.0), decimals=3)
        
        saveName = "Dataset/" + str(gamma) + "_" + str(center) + "_" + str(amplitude) + ".csv"
        
        x,y = generateData(gamma, center, -10, 10, 100, amplitude) #generates the lorentzian
        y_noisy = addWhiteNoiseRandom(x, y, 0.2) #adds random white noise by factor
        
        # Round the data to at most 5 decimal places
        x_rounded = np.around(x, decimals=5)
        y_rounded = np.around(y_noisy, decimals=5)
        
        saveData(x, y_noisy, saveName)
        #showData(x_rounded, y_rounded)


if __name__ == "__main__":
    main()

