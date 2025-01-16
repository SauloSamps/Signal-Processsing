import os
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
    
    
def generateData(gamma, x0, xmin, xmax, numberOfPoints, height):
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
    
    
def addWhiteNoiseRandom(xData, yData, factor):
    y_noisy = yData + np.random.normal(0, factor, len(xData))
    return y_noisy
    

def generateFit(gamma, x0, xmin, xmax, numberOfPoints, height):
    x = np.linspace(xmin, xmax, numberOfPoints)  # Generate x-values
    y = lorentzian(x, x0, gamma, height)  # Calculate y-values
    return x,y
    
    
def generateCurves(gamma, x0, xmin, xmax, numberOfPoints, height, noiseRange, totalNoiseDatapoints, curvesPerNoise, saves=0):
    
    for i in range(totalNoiseDatapoints):
        os.mkdir("Dataset/" + str(i/noiseRange))
        for j in range(curvesPerNoise):
            x,y = generateData(gamma, x0, xmin, xmax, numberOfPoints, height) #generates the lorentzian
            y_noisy = addWhiteNoiseRandom(x, y, i/noiseRange) #adds random white noise by factor
            saveData(x, y_noisy, "Dataset/" + str(i/noiseRange) + "/" + str(j) + ".csv")
    

def dataset(filename):
    #OPENS THE DATASET
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    return data

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
    
    
def saveData(xData, yData, name):
    # Save (x, y) data to a CSV file
    data = np.column_stack((xData, yData))
    np.savetxt(name, data, delimiter=',', fmt='%.5f,%.5f', header='x,y', comments='')
    
    
def analyzeDataset(dataset, method):

    errors = []
    for curve in dataset:
        x = curve["data"][0]
        y = curve["data"][1]
        noise = curve["noise"]

        params = create_params(center=5, gamma=1, amplitude=5)
        out = minimize(lorentzian_residual, params, method=method, args=(x,), kws={'data': y})
        
        error = {"noise": noise, "stderror": out.params['center'].stderr}
        errors.append(error)
    
    x_error = []
    y_error = []
    
    noise_levels = set(error["noise"] for error in errors)
    
    for noise in noise_levels:
        counter = 0
        accumulator = 0
        for error in errors:
            if(error["noise"] == noise):
                counter += 1
                accumulator += abs(error["stderror"])
        x_error.append(noise)
        y_error.append(accumulator/counter)
    
    return x_error, y_error
    
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
    
def showError(x, y_amplitude, y_center, y_gamma, title, xlabel, ylabel, filename):
    plt.scatter(x, y_amplitude, label='Amplitude', color='r', s=5)
    plt.scatter(x, y_center, label='Center', color='g', s=5)
    plt.scatter(x, y_gamma, label='Gamma', color='b', s=5)
    #plt.scatter(x, y_height, label='Height', color='black', s=5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.ylim(0, 10)
    #plt.show()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.clf()
    
def showErrorSeparate(x, y_value, name, color):
    plt.scatter(x, y_value, label=name, color=color, s=5)
    plt.xlabel('Noise Level')
    plt.ylabel('Error')
    plt.title('Fit Error by Noise')
    plt.legend()
    #plt.ylim(0, 1)
    #plt.show()
    plt.savefig(name + "Error.png", dpi=300, bbox_inches='tight')
    plt.clf()
    
    
def runFittingAlg(noiseRange, totalNoiseDatapoints, curvesPerNoise, method):
    y_amplitude = []
    y_gamma = []
    y_center = []
    y_height = []
    fails = []
    
    for i in range(0,totalNoiseDatapoints):
        
        amplitude_error_mean = 0
        gamma_error_mean = 0
        center_error_mean = 0
        counter = 0
        fail_counter = 0
        #height_error_mean = 0
        
        amplitude_error_median = []
        gamma_error_median = []
        center_error_median = []
        
        histogram_targets = [0.1,0.4,0.7,0.9]
        amplitude_histogram = []
        gamma_histogram = []
        center_histogram = []
        
        for j in range(0,curvesPerNoise):
            
            signal = dataset("Dataset/" + str(i/noiseRange) + "/" + str(j) + ".csv")
            x = signal[:, 0]
            y = signal[:, 1]
            
            
            params = create_params(center=1, gamma=1, amplitude=1)
            out = minimize(lorentzian_residual, params, method=method, args=(x,), kws={'data': y})
            
            
            amplitude_error = out.params['amplitude'].stderr
            gamma_error = out.params['gamma'].stderr
            center_error = out.params['center'].stderr
            #height_error = out['height'].stderr
            
            amplitude = out.params['amplitude'].value
            gamma = out.params['gamma'].value
            center = out.params['center'].value
            
            if amplitude_error != None and gamma_error != None and center_error != None:
                
                """
                amplitude_error_mean += amplitude_error
                gamma_error_mean += gamma_error
                center_error_mean += center_error
                """
                #height_error_mean += height_error
                
                """
                if (j%500 == 0 and j!=0):
                    x_fit,y_fit = generateFit(values['sigma'], values['center'], -10, 10, 100, values['height'])
                    showFit(x_fit, y_fit, x, y, i)
                    showData(x,y,i)
                """
                
                amplitude_error_median.append(amplitude_error)
                gamma_error_median.append(gamma_error)
                center_error_median.append(center_error)
                
                amplitude_histogram.append(amplitude)
                gamma_histogram.append(gamma)
                center_histogram.append(center)
                
                counter += 1
            else:
                fail_counter += 1
    
        if fail_counter > 0:
            fail = {"noise": i/noiseRange, "fails": fail_counter}
            fails.append(fail)
        
        """
        amplitude_error_mean = amplitude_error_mean/counter
        gamma_error_mean = gamma_error_mean/counter
        center_error_mean = center_error_mean/counter
        #height_error_mean = height_error_mean/counter
        """
        
        amplitude_error_median = np.median(amplitude_error_median)
        gamma_error_median = np.median(gamma_error_median)
        center_error_median = np.median(center_error_median)
        
        #amplitude_error_mean = amplitude_error_mean/np.pi
        
        """
        y_amplitude.append(np.around(amplitude_error_mean, decimals=5))
        y_gamma.append(np.around(gamma_error_mean, decimals=5))
        y_center.append(np.around(center_error_mean, decimals=5))
        #y_height.append(np.around(height_error_mean, decimals=5))
        """
        
        y_amplitude.append(np.around(amplitude_error_median, decimals=5))
        y_gamma.append(np.around(gamma_error_median, decimals=5))
        y_center.append(np.around(center_error_median, decimals=5))
        
        if (i/noiseRange) in histogram_targets:
        
            # Calculate the first and third quartile (Q1, Q3)
            Q1 = np.percentile(amplitude_histogram, 25)
            Q3 = np.percentile(amplitude_histogram, 75)

            # Calculate the Interquartile Range (IQR)
            IQR = Q3 - Q1

            # Define outlier thresholds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Remove the outliers
            filtered_values = [value for value in amplitude_histogram if lower_bound <= value <= upper_bound]
        
        
        
            plt.hist(filtered_values, bins=25, edgecolor='black')  # Adjust 'bins' as needed

            # Add a title and labels
            plt.title('Histogram of Amplitude Values')
            plt.xlabel('Amplitude')
            plt.ylabel('Frequency')
            
            plt.savefig("histogram-" + str(i/noiseRange) + ".png", dpi=300, bbox_inches='tight')
            plt.clf()
        
        
    return y_amplitude, y_gamma, y_center, fails
    