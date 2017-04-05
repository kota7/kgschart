# -*- coding: utf-8 -*- 

from colors import BEIGE, BLACK, GRAY
from utils import rgb_dist, to_gray
import numpy as np


class Yaxis:
    image = None
    nlabels = None

    def __init__(self, image):
        self.image = image
    

    def get_label_range(self):
        """
        Returns the min and max of y-axis labels

        Returns
          tuple of strings such as (2k, 1d)
        """
        return () 


    def get_label_arrays(self, positions):
        """
        make Y-axis labal data

        Args
          positions: expected indices of labels. If provided,
                     the search becomes more efficient

        Returns
          list of (list of 2d-arrays) or None, where (i,j) element indicates
          the j-th letter of i-th label.  
          (r, c) element of the 2d-array is the gray scale of cell (r,c) 
        """
        image = self.image
        if image is None: return []
        if image.size == 0: return []

        thres_dist = 0.1
        thres_frac = 0.95


        def is_background(arr):
            dist = rgb_dist(arr, BEIGE)
            frac = np.mean(dist < thres_dist)
            return frac >= thres_frac
        

        # extract labels rows
        # start from position and expand the area up and down
        # until we hit background
        labels = []
        index_checked = [False] * image.shape[0]
        for p in positions:
            index_to_check = [p]
            i1 = image.shape[0]
            i2 = -1
            while len(index_to_check) > 0:
                i = index_to_check.pop()
                index_checked[i] = True

                flg = is_background(image[i]) 
                if not flg:
                    # new non-background is found so exand the area
                    i1 = min(i1, i)
                    i2 = max(i2, i)

                    if i-1 >= 0 and not index_checked[i-1]:
                        index_to_check.append(i-1)
                    if i+1 < image.shape[0] and not index_checked[i+1]:
                        index_to_check.append(i+1) 
            if i1 <= i2:
                print(i1, i2)
                labels.append(image[i1:(i2+1)])
            else: 
                labels.append(None)

        # split labels into letters
        def split_to_letters(label):
            if label is None: return None
            dist = rgb_dist(label, BEIGE)
            frac = np.mean(dist < thres_dist, axis=0)
            is_background = (frac >= thres_frac)
            start = np.where(np.logical_and(
                np.logical_not(is_background),
                np.append(True, is_background[0:-1])))[0]
            end = np.where(np.logical_and(
                np.logical_not(is_background),
                np.append(is_background[1:], True)))[0] + 1
            return [label[:, a:b] for a,b in zip(start, end)]
        letters = [split_to_letters(label) for label in labels]
        

        # convert to gray scale 
        for j in range(len(letters)):
            if letters[j] is None: continue
            for k in range(len(letters[j])):
                letters[j][k] = to_gray(letters[j][k], BEIGE, GRAY)

        return letters
    

    def extract_letters(self):
        """
        extract all sub images of letters 

        Returns
          list of numpy arrays of shape (nrow, ncol)
          each element is the gray scale of the cell
        """
        image = self.image
        if image is None: return []
        if image.size == 0: return []

        thres_dist = 0.1
        thres_frac = 0.95
        
        dist = rgb_dist(image, BEIGE)
        is_beige = (dist < thres_dist)


        # identify rows of labels 
        frac = np.mean(is_beige, axis=1)
        is_bg_row = (frac >= thres_frac)
        row1 = np.where(np.logical_and(
            np.logical_not(is_bg_row),
            np.append(True, is_bg_row[0:-1])))[0]
        row2 = np.where(np.logical_and(
            np.logical_not(is_bg_row),
                np.append(is_bg_row[1:], True)))[0] + 1
        
        def split_letters(i1, i2):
            frac = np.mean(is_beige[i1:i2], axis=0)
            is_bg_col = (frac >= thres_frac)
            start = np.where(np.logical_and(
                np.logical_not(is_bg_col),
                np.append(True, is_bg_col[0:-1])))[0]
            end = np.where(np.logical_and(
                np.logical_not(is_bg_col),
                np.append(is_bg_col[1:], True)))[0] + 1
            return [image[i1:i2, a:b] for a,b in zip(start, end)]

        out = [split_letters(a,b) for a,b in zip(row1, row2)]
        # flatten 
        out = sum(out, [])


        # convert to gray scale
        out = [to_gray(o, BEIGE, GRAY) for o in out]
        return out

        

