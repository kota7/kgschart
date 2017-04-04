# -*- coding: utf-8 -*- 

import numpy as np

def rgb_dist(arr, col):
    """
    Compute the Eucledean distance between colors defined by RGB
    
    Args
       arr: numpy array of shape (nrow, ncol, 3)
       col: numpy array of shape (3)
    
    Returns:
       numpy array of shape (nrow, ncol). Each element represents 
       the distance between the corresponding element in arr from col,
       scaled between from 0 (closest) to 1 (farthest)    
    """
    tmp = np.power(arr - col, 2.0)
    # weight by [2,4,3]: c.f. https://en.wikipedia.org/wiki/Color_difference
    tmp = tmp * np.array([2.0/9, 4.0/9, 3.0/9])  
    tmp = np.sum(tmp, axis=len(tmp.shape)-1)
    tmp = np.power(tmp, 0.5)
    return tmp/255.0

