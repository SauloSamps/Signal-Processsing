import numpy as np
import matplotlib.pyplot as plt

def lorentzian(x, x0, gamma, maximum):
    #x0 is the center for the curve
    #gamma is the width of the curve
    #maximum is the amplitude
    
    #maximum = maximum * np.pi
    #return (maximum/np.pi) * (gamma / ((x - x0)**2 + gamma**2))
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

def saveData(xData, yData):
    # Save (x, y) data to a CSV file
    data = np.column_stack((xData, yData))
    np.savetxt('lorentzian_data.csv', data, delimiter=',', fmt='%.5f,%.5f', header='x,y', comments='')
    
def showData(xData, yData):
    plt.scatter(xData, yData, label='Data Points', color='r', s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Lorentzian Curve with Noise')
    plt.legend()
    plt.show()

def main():
    
    x,y = generateData(1, 0, -10, 10, 100, 10) #generates the lorentzian
    y_noisy = addWhiteNoiseRandom(x, y, 0.1) #adds random white noise by factor
    
    # Round the data to at most 5 decimal places
    x_rounded = np.around(x, decimals=5)
    y_rounded = np.around(y_noisy, decimals=5)
    
    saveData(x, y_noisy)
    showData(x_rounded, y_rounded)


if __name__ == "__main__":
    main()

