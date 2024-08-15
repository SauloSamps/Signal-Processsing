from Content.Scripts.dataset import Dataset

class Controller():
    def __init__(self):
        self.dataset = Dataset()
    
    def generate_data(self, args):

        self.dataset.generate_lorentzian_dataset_area()