# -*- coding: utf-8 -*-


from PIL import Image
import os
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
from datetime import timedelta

from .colors import BLACK, WHITE, BEIGE, GRAY, GREEN
from .utils import rgb_dist, detect_consecutive_true, str_to_num_rank
from .parts import Yaxis, Caption, Graph


# on python3, we can multiply timedelta and float
# we cannot do so on python2, so write a bit of code
PY3 = (sys.version_info[0] == 3)


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


    # horizontal and vertical range
    rank_range = ()  # e.g. (2k, 3d)
    time_range = ()  # e.g. (2013-04-03, 2014-05-12)

    # output data
    data = None


    def __init__(self, imagefile):        
        self.image = np.asarray(Image.open(imagefile))
        self.tblr = self.detect_graph_area()
        
        im = self.image
        t,b,l,r = self.tblr

        if b-t > 0 and r-l > 0:
            self.graph = Graph(im[t:b, l:r])
            self.yaxis = Yaxis(im[:, 0:(l-1)]) 
            self.caption = Caption(im[0:(t-1), l:r])

    
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
        #print('num grids', ngrids)
        
        positions = None
        if ngrids is not None:
            top = self.tblr[0]
            bottom = self.tblr[1]
            step = (bottom-top)//(ngrids+1)
            positions = list(range(top, bottom+1, step)) 
        #print('positions', positions)

        # obtain the rank range from yaxis
        self.set_rank_range(self.yaxis.get_rank_range(positions)) 
        #print('rank range', self.rank_range)
        
        # obtain date-time range from caption
        self.set_time_range(self.caption.get_time_range())    
        #print('time range', self.time_range)

        # compile data
        self.data = self.make_data()

    def make_data(self):
        """
        Compile and return data frame
        """
        y = self.line_index
        n = len(y)
        if n == 0: 
            #  empty dataframe if line index is empty 
            return pd.DataFrame(dict(time=[], rate=[]))
        if n == 1:
            # this won't happen for normal input 
            # just write this so that the later computation
            # never raises error
            return pd.DataFrame(dict(time=[np.nan], rate=y))
        
        # scale y
        if len(self.rank_range) != 2:
            y = -y 
        else:
            y1,y2 = [str_to_num_rank(r) for r in self.rank_range]
            if np.isnan(y1) or np.isnan(y2):
                y = -y
            else:
                z2 = 0
                z1 = self.tblr[1] - self.tblr[2]
                # (z1, z2) <-> (y1, y2)
                b = (y2-y1)/(z2-z1)
                a = y1-b*z1
                y = a + b*(y+0.5)
        
        # scale x
        #print(self.time_range)
        if len(self.time_range) != 2:
            x = np.arange(n)
        else:
            x1,x2 = self.time_range 
            b = (x2-x1)/n 
            if PY3:
                x = x1 + (np.arange(n)+0.5)*b
            else:
                x = np.array([x1 + timedelta(seconds=b.total_seconds()*(0.5+i)) for i in range(n)])

        return pd.DataFrame(dict(time=x, rate=y), columns=['time', 'rate'])
        
    def update_data(self):
        self.data = self.make_data()
    
        
    def extract_label_letters(self):
        if self.yaxis is None: return []
        return self.yaxis.extract_letters()

    def extract_caption_letters(self):
        if self.caption is None: return []
        return self.caption.extract_letters()


    # functions to set range for x and y axis
    # can be used for user specification as well
    def set_time_range(self, time_range):
        self.time_range = time_range
    
    def set_rank_range(self, rank_range):
        self.rank_range = rank_range

    
    # plot image and parts
    # mainly for debugging
    def plot_image(self):
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
        if self.caption is not None:
            plt.subplot(224)
            self.caption.plot(False)
        plt.show()


    def plot_data(self, block=True):
        if self.data is None: 
            plt.plot()
            plt.show()
            return
        plt.plot(self.data['time'], self.data['rate'])
        plt.grid()
        plt.show(block)






