# -*- coding: utf-8 -*-


from PIL import Image
import os
import numpy as np
from matplotlib import pyplot as plt

from colors import BLACK, WHITE, BEIGE, GRAY, GREEN
from utils import rgb_dist, detect_consecutive_true
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
    tblr = [0,0,0,0]


    # line_index: numpy array whose size equals the ncol
    #             each element indicates the index of graph line
    #             within the graph area
    line_index = np.empty(0)


    # graph, caption, yaxis: sub image class objects
    graph = None
    caption = None
    yaxis = None


    def __init__(self, imagefile):
        if  not os.path.exists(imagefile): 
            raise IOError('No such file exists: "%s"' % imagefile)
        
        self.image = np.asarray(Image.open(imagefile))
        self.tblr = self.detect_graph_area()
        
        im = self.image
        t,b,l,r = self.tblr

        if b-t > 0 and r-l > 0:
            self.graph = Graph(im[t:b, l:r])
            self.yaxis = Yaxis(im[:, 0:(l-1)]) 
            

    
    def detect_graph_area(self):
        """
        Identify three key areas within the image
        returns a 4-dim list of integers of graph boundary
        """
        if self.image is None: return [0,0,0,0]

        im = self.image
        
        # strategy: find a box white 
        thres_dist = 0.05

        # find white rows
        dist = rgb_dist(im[:, im.shape[1]//2], WHITE)
        white_rows = (dist < thres_dist)
        i1,i2 = detect_consecutive_true(white_rows)
        # if there is a graph, there must be two white rows
        if len(i1) != 2: return [0,0,0,0]
        top = i2[0]
        bottom = i1[1]

        # find white cols
        dist = rgb_dist(im[im.shape[0]//2], WHITE)
        white_cols = (dist < thres_dist)
        j1,j2 = detect_consecutive_true(white_cols)
        # if there is a graph, there must be two white rows
        if len(j1) != 2: return [0,0,0,0]
        left = j2[0]
        right = j1[1]

        return [top, bottom, left, right]

    

    def parse(self):
        if self.image is None: return

        if self.graph is None: return 
        # obtain the line graph height
        self.line_index = self.graph.get_line_index()

        # obtain number of grid lines
        # this helps to detect y-axis labels
        ngrids = self.graph.get_num_grids()
        print('num grids', ngrids)
        
        positions = None
        if ngrids is not None:
            top = self.tblr[0]
            bottom = self.tblr[1]
            step = (bottom-top)//(ngrids+1)
            positions = list(range(top, bottom+1, step)) 
        print('positions', positions)
    

    def extract_label_letters(self):
        if self.yaxis is None: return []
        return self.yaxis.extract_letters()


    
    def plot(self):
        plt.subplot(221)
        plt.plot(1)
        
        if self.image is not None:
            plt.subplot(221)
            plt.imshow(self.image)
        if self.yaxis is not None:
            plt.subplot(222)
            self.yaxis.plot(False)
        if self.graph is not None:
            plt.subplot(223)
            self.graph.plot(False)
        plt.show()


