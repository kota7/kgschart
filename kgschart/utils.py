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



def to_gray(arr, white, black):
    """
    Convert RGB color array in to gray scale, 
    using specified white and black as the two polars
    
    Args
       arr:   numpy array of shape (nrow, ncol, 3)
       white: numpy array of size 3, benchmark for the largest color
       black: numpy array of size 3, benchmark for the smallest color
    
    Returns
        numpy array of shape (nrow, ncol), each element is the degree of 
        the color relative to white and black
    """
    
    # weight by [2,4,3]: c.f. https://en.wikipedia.org/wiki/Color_difference
    weights = np.power(np.array([2.0/9, 4.0/9, 3.0/9]), 0.5)
    white2 = white * weights
    black2 = black * weights
    arr2 = arr * weights
    
    denom = float(np.dot(black2 - white2, black2 - white2))
    out = np.dot(arr2 - black2, white2 - black2) / denom
    return out
    
    