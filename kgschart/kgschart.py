# -*- coding: utf-8 -*-


from PIL import Image
import os
import numpy as np
from matplotlib import pyplot as plt

from colors import BLACK, WHITE, BEIGE, GRAY, GREEN
from utils import rgb_dist
from yaxis import Yaxis
from caption import Caption
from graph import Graph





class KgsChart:

    # image: original image in RGB array 
    #        assumed to be of shape (nrow, ncol, 3)
    image = None

    # tbrl: 4-dim list of the indices of graph boundary
    #       [top, bottom, right, left]
    #       i.e. image[top:bottom][right:left] is the graph
    tbrl = [0,0,0,0]


    # line_index: numpy array whose size equals the ncol
    #             each element indicates the index of graph line
    #             within the graph area
    line_index = np.empty(0)


    def __init__(self, imagefile):
        if  not os.path.exists(imagefile): 
            raise IOError('No such file exists: "%s"' % imagefile)
        
        self.image = np.asarray(Image.open(imagefile))
        self.tbrl = self.detect_graph_area()
        
        im = self.image
        t,b,r,l = self.tbrl
        self.graph = Graph(im[t:b, r:l])
        

    
    def detect_graph_area(self):
        """
        Identify three key areas within the image
        returns a 4-dim list of integers of graph boundary
        """
        if self.image is None: return [0,0,0,0]

        # define im to reduce writing
        im = self.image

        def mostly_black_or_gray(arr, thres_dist, theres_frac):
            dist_from_black = rgb_dist(arr, BLACK)
            dist_from_gray  = rgb_dist(arr, GRAY)
            dist = np.minimum(dist_from_black, dist_from_gray)
            frac = np.mean(dist < thres_dist)
            return frac >= thres_frac

        # threshold for color distance and fraction
        # define here because they are used repeatedly
        thres_dist = 0.2
        thres_frac = 0.8

        # check if the middle of the image is mostly black or gray
        # if not, then there is no graph
        mid_row = im.shape[0]//2
        if not mostly_black_or_gray(im[mid_row], thres_dist, thres_frac):
            # image has no graph
            return [im.shape[0]//2, im.shape[0]//2,\
                    im.shape[1]//2, im.shape[1]//2]
        
        # binary search to find top
        # top is largest i such that
        # im[i] is mostly black or gray 
        # we use for-loop instead of while true since
        # we know that n is below 1000, so 2^10 would be enough
        i0 = 0
        i1 = mid_row
        for _ in range(10): 
            if i0 >= i1:
                top = i1
                break
            mid = (i0+i1)//2
            if mostly_black_or_gray(im[mid], thres_dist, thres_frac):
                i1 = mid
            else:
                i0 = mid + 1
        
        # binary search to find bottom
        # bottom is smallest i such that
        # im[i] is not mostly black or gray
        i0 = mid_row
        i1 = im.shape[0]-1
        for _ in range(10):
            if i0 >= i1:
                bottom = i1
                break
            mid = (i0+i1)//2
            if mostly_black_or_gray(im[mid], thres_dist, thres_frac):
                i0 = mid + 1
            else:
                i1 = mid

        # before starting the search for right and left,
        # make sure that mid col is mostly black
        # otherwise, regard there is no graph
        mid_col = im.shape[1]//2
        if not mostly_black_or_gray(im[:,mid_col], thres_dist, thres_frac):
            # image has no graph
            return [im.shape[0]//2, im.shape[0]//2,\
                    im.shape[1]//2, im.shape[1]//2]

        # binary search for right,
        # which is the smallest j such that
        # im[:,j] is mostly black or gray
        j0 = 0
        j1 = mid_col
        for _ in range(10):
            if j0 >= j1:
                right = j1
                break
            mid = (j0+j1)//2
            if mostly_black_or_gray(im[:,mid], thres_dist, thres_frac):
                j1 = mid
            else:
                j0 = mid + 1

        # binary search for left,
        # i.e. the smallest j such that
        # im[:,j] is not mostly black or gray
        j0 = mid_col 
        j1 = im.shape[1]-1
        for _ in range(10):
            if j0 >= j1:
                left = j1
                break
            mid = (j0+j1)//2
            if mostly_black_or_gray(im[:,mid], thres_dist, thres_frac):
                j0 = mid + 1
            else:
                j1 = mid

        return [top, bottom, right, left]

    

    def parse(self):
        if self.image is None: return

        # obtain the line graph height
        self.line_index = self.graph.get_line_index()

        # obtain number of grid lines
        # this helps to detect y-axis labels
        ngrids = self.graph.get_num_grids()
        print(ngrids)


    
    def display(self):
        """
        Display original image
        """
        plt.imshow(self.image)
        plt.show()



# quick test code below (to be deleted later)
k = KgsChart('../data/images/kotakun-ja_JP.png')
print(k.tbrl)
k.parse()
#plt.plot(-k.line_index)
plt.show()


#k.display()


k = KgsChart('../data/images/Quinton-ja_JP.png')
print(k.tbrl)
k.parse()

k = KgsChart('../data/images/Zen19L-ja_JP.png')
print(k.tbrl)
k.parse()
#plt.plot(-k.line_index)
plt.show()
