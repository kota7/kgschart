# -*- coding: utf-8 -*- 

import numpy as np

from utils import rgb_dist
from colors import GREEN, GRAY


class Graph:
    image = None
    def __init__(self, image):
        self.image = image

    def get_num_grids(self):
        """
        Detect the number of gird lines
        """
        im = self.image
        if im is None or im.shape[0] < 1 or im.shape[1] < 1: 
            return None 

        thres_dist = 0.2
        thres_frac = 0.9
        mostly_gray = (rgb_dist(im, GRAY) < thres_dist)
        frac = np.mean(mostly_gray, axis=1)
        gray_index = (frac > thres_frac).nonzero()[0]

        if len(gray_index) == 0: return 0
        return 1 + np.sum(np.diff(gray_index) > 1)


    def get_line_index(self):
        """
        Detect line position in the graph image

        Returns
          numpy array of the same length as the image's width
        """

        im = self.image
        if im is None or im.shape[0] < 1 or im.shape[1] < 1: 
            return np.empty(0) 

        
        # compute distance from green, black, gray and find the
        # cells that are closest to green
        dist_green = rgb_dist(im, GREEN)
        thres_dist = 0.35

        # change distance of cells for enough from green to 1
        # later, if colwise minimum is 1, 
        # then the column is regarded as having no line
        dist_green[dist_green > thres_dist] = 1.0  

        min_dist = np.min(dist_green, axis=0)
        has_line = np.where(min_dist < 1.0)[0]

        # initialize
        out = np.empty(im.shape[1]) 
        out[:] = np.nan
        for j in has_line:
            min_index = np.where(dist_green[:,j] == min_dist[j])[0]
            out[j] = np.mean(min_index)
            #out[j] = np.average(np.arange(im.shape[0]),\
            #                    weights=1.0-dist_green[:,j])

        return out

