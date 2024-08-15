import matplotlib as plt

class Curve:
    def __init__(self):
        self.x = []
        self.y = []
        self.y_fit = []
    
    def set_curve(self, datapoints):
        self.x = datapoints[0]
        self.y = datapoints[1]

    def set_fit(self, y_fit):
        self.y_fit = y_fit

    def get_curve(self):
        return self
    
    def save_curve(self,name="example"):
        plt.scatter(self.x, self.y, label='Data Points', color='r', s=5)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(name)
        plt.legend()
        plt.savefig(name + ".png", dpi=300, bbox_inches='tight')
        plt.clf()