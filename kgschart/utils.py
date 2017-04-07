# -*- coding: utf-8 -*- 

import numpy as np
import re

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
    
    
def detect_consecutive_false(arr):
    return detect_consecutive_true(np.logical_not(arr))


def detect_consecutive_true(arr):
    """
    returns the tuple of two index vectors, (start, end) 
    where for each pair from (i,j) from (start,end), 
    arr[i:j] are all true.

    Args
        arr: 1d array of logicals
    
    Returns
        2-tuple of integer arrays of same size
    """
    if len(arr.shape) != 1:
        print("array must be 1-dimensional")
        raise
    if arr.shape[0] < 1: return []
    start = np.where(np.logical_and(
        arr, np.logical_not(np.append(False, arr[0:-1]))))[0]
    end = np.where(np.logical_and(
        arr, np.logical_not(np.append(arr[1:], False))))[0] + 1
    if len(start) != len(end):
        print("unexpected error")
        raise
    return (start, end)


def pad_image(arr, target_rows, target_cols, value):
    """
    pad a certain value to arr so that the size becomes
    target_rows and target_cols
    raise error if the size of arr is smaller than the target
    
    Args
      arr: numpy array of shape (nrow, ncol)
      target_rows: desired vertical size
      target_cols: desired horizontal size
      value: value to be padded
    
    Returns
      numpy array
    """
    rows_toadd = target_rows - arr.shape[0]
    if rows_toadd < 0: 
        print("array is already larger than target rows")
        raise
    row_added1 = rows_toadd // 2
    row_added2 = rows_toadd - row_added1
    
    cols_toadd = target_cols - arr.shape[1]
    if cols_toadd < 0:
        print("array is already larger than target cols")
        raise
    col_added1 = cols_toadd // 2
    col_added2 = cols_toadd - col_added1
    
    out = np.pad(arr, ((row_added1, row_added2), (col_added1, col_added2)), 
                 mode='constant', constant_values=value)
    return out
    



def str_to_num_rank(str_rank):
    str_rank = str_rank.lower().strip()
    r = re.search(r'^(\d)([dk])$', str_rank)
    if r is None: return np.nan
    n = int(r.group(1))
    t = r.group(2)
    out = -n if t == 'k' else n-1
    return out

def num_to_str_rank(num):
    out = str(-num) + 'k' if num < 0 else str(num+1) + 'd'
    return out




