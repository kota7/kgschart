# -*- coding: utf-8 -*- 


import numpy as np
from matplotlib import pyplot as plt

from utils import rgb_dist, detect_consecutive_false, to_gray
from colors import BEIGE, GRAY


class Caption:
    image = None
    
    def __init__(self, image):
        self.image = image
        
    def plot(self, show=True):
        if self.image is None: return
        plt.imshow(self.image)
        if show: plt.show()

    def extract_letters(self):
        """
        extract all sub images of letters

        Returns
          list of numpy arrays of shape(nrow,ncol)
          each element is an image array.
          if asgray: each element is (nrow, ncol) shape
          otherwise: each element is (nrow, ncol, channel) shape
        """
        image = self.image
        if image is None: return []
        if image.size ==0: return []

        thres_dist = 0.1
        thres_frac = 1.0 

        dist = rgb_dist(image, BEIGE)
        is_beige = (dist < thres_dist)

        # find rows that have non-background 
        not_bg_row = (np.mean(is_beige, axis=1) < thres_frac)
        if not np.any(not_bg_row): return []  # all background
        # the first and last index of non-background
        index = not_bg_row.nonzero()[0]
        i1 = index[0]
        i2 = index[-1]
        
        # split into letters  
        frac = np.mean(is_beige[i1:(i2+1)], axis=0)
        is_bg_col = (frac >= thres_frac)
        start, end = detect_consecutive_false(is_bg_col)

        out = [image[i1:(i2+1), a:b] for a,b in zip(start, end)]
        
        # to gray scale
        for i in range(len(out)):
            out[i] = to_gray(out[i], BEIGE, GRAY)
        
        return out
        

