import numpy as np
import matplotlib.pyplot as plt
from curve import Curve

class Dataset:
    def __init__(self):
        self.data = []

    def lorentzian(self, x, x0, gamma, maximum):
        return maximum / (1 + ((x - x0) / gamma)**2)
    
    def addWhiteNoiseRandom(self, xData, yData, factor):
        y_noisy = yData + np.random.normal(0, factor, len(xData))
        return y_noisy
    
    def generate_lorentzian_with_area(self, area, x_range, num_points):
        """
        Generates a Lorentzian curve with a specified total area.

        Parameters:
        - area (float): Desired total area under the Lorentzian curve.
        - x_range (tuple): Range of x-values for the curve (default is (-10, 10)).
        - num_points (int): Number of points to generate for the curve (default is 1000).

        Returns:
        - x (numpy array): x-values for the Lorentzian curve.
        - y (numpy array): y-values for the Lorentzian curve.
        """

        # Randomly choose the peak position and HWHM
        x0 = np.random.uniform(x_range[0], x_range[1])
        gamma = np.random.uniform(0.1, 5.0)  # You can adjust this range

        # Adjust gamma to make sure the area is as desired
        gamma = area * np.pi / gamma

        # Generate x values
        x = np.linspace(x_range[0], x_range[1], num_points)
        
        # Calculate the Lorentzian curve
        y = (gamma / np.pi) / ((x - x0)**2 + gamma**2)
        
        # Normalize the curve to have the specified area
        y *= area / np.trapz(y, x)
        
        return x, y
    

        """
        A/
        """
    
    def generate_lorentzian_dataset_area(self, area=1, noise_range=(0,1), num_noise_levels=100, num_samples=1000, num_points=100, x_range=(-10, 10)):
        noise_levels =  np.linspace(noise_range[0], noise_range[1], num_noise_levels)
        for noise in noise_levels:
            single_noise_dataset = []
            for i in range(num_samples):
                curve = Curve()
                x,y = self.generate_lorentzian_with_area(area, x_range, num_points)
                y_noisy = self.addWhiteNoiseRandom(x, y, noise)
                curve.set_curve((x, y_noisy))
                single_noise_dataset.append(curve)
            self.data.append({"noise": noise, "curves":single_noise_dataset})

