# -*- coding: utf-8 -*- 


import numpy as np
from matplotlib import pyplot as plt


class Caption:
    image = None
    
    def __init__(self, image):
        self.image = image
        
    def plot(self, show=True):
        if self.image is None: return
        plt.imshow(self.image)
        if show: plt.show()
