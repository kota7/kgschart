# -*- coding: utf-8 -*- 


import re
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

from .utils import rgb_dist, detect_consecutive_false, to_gray
from .utils import str_to_num_rank, num_to_str_rank
from .colors import BEIGE, GRAY, GREEN, BLACK
from .classifiers import LabelClassifier, CaptionJaClassifier, CaptionEnClassifier





class Graph:
    image = None
    def __init__(self, image):
        self.image = image
    
    def plot(self, show=True):
        if self.image is None: return
        plt.imshow(self.image)
        if show: plt.show()
         
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

        out = np.empty(im.shape[1]) 
        out[:] = np.nan
        for j in has_line:
            min_index = np.where(dist_green[:,j] == min_dist[j])[0]
            out[j] = np.mean(min_index)
            #out[j] = np.average(np.arange(im.shape[0]),\
            #                    weights=1.0-dist_green[:,j])

        return out





# this is shared by all instances of Yaxis
label_classifier = LabelClassifier()

class Yaxis:
    image = None
    nlabels = None

    def __init__(self, image):
        self.image = image
        self.classifier = label_classifier

    
    def plot(self, show=True):
        if self.image is None: return
        plt.imshow(self.image)
        if show: plt.show()


    def get_rank_range(self, positions):
        """
        Returns the min and max of y-axis labels

        Args
          positions: expected indices of labels. 

        Returns
          tuple of strings such as (2k, 1d)
        """
        label_list = self.get_label_list(positions)
        ranks = ['' if l is None else self.classifier.predict(l) \
                 for l in label_list]

        # look for the max rank from the top
        max_rank = None
        i = 0
        while i < len(ranks):
            if ranks[i] == '':
                i += 1
                continue
            n = str_to_num_rank(ranks[i])
            if not np.isnan(n):
                max_rank = num_to_str_rank(n+i)
                break
            i += 1
        if max_rank is None: return ()

        # look for the min rank from the bottom
        min_rank = None
        i = 0
        while i < len(ranks):
            j = len(ranks)-i-1
            if ranks[j] == '':
                i += 1
                continue
            n = str_to_num_rank(ranks[j])
            if not np.isnan(n):
                min_rank = num_to_str_rank(n-i)
                break
            i += 1
        if min_rank is None: return ()

        return (min_rank, max_rank)
         


    def get_label_list(self, positions):
        """
        make Y-axis labal data

        Args
          positions: expected indices of labels. 

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
            #start = np.where(np.logical_and(
            #    np.logical_not(is_background),
            #    np.append(True, is_background[0:-1])))[0]
            #end = np.where(np.logical_and(
            #    np.logical_not(is_background),
            #    np.append(is_background[1:], True)))[0] + 1
            start, end = detect_consecutive_false(is_background)
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
        #row1 = np.where(np.logical_and(
        #    np.logical_not(is_bg_row),
        #    np.append(True, is_bg_row[0:-1])))[0]
        #row2 = np.where(np.logical_and(
        #    np.logical_not(is_bg_row),
        #        np.append(is_bg_row[1:], True)))[0] + 1
        row1, row2 = detect_consecutive_false(is_bg_row)
        
        def split_letters(i1, i2):
            frac = np.mean(is_beige[i1:i2], axis=0)
            is_bg_col = (frac >= thres_frac)
            #start = np.where(np.logical_and(
            #    np.logical_not(is_bg_col),
            #    np.append(True, is_bg_col[0:-1])))[0]
            #end = np.where(np.logical_and(
            #    np.logical_not(is_bg_col),
            #    np.append(is_bg_col[1:], True)))[0] + 1
            start, end = detect_consecutive_false(is_bg_col)
            return [image[i1:i2, a:b] for a,b in zip(start, end)]

        out = [split_letters(a,b) for a,b in zip(row1, row2)]
        # flatten 
        out = sum(out, [])


        # convert to gray scale
        out = [to_gray(o, BEIGE, GRAY) for o in out]
        return out

        



# classifiers shared by all instances
caption_ja_classifier = CaptionJaClassifier()
caption_en_classifier = CaptionEnClassifier()

class Caption:
    image = None
    
    def __init__(self, image):
        self.image = image
        self.classifier_ja = caption_ja_classifier
        self.classifier_en = caption_en_classifier
        
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

        thres_dist = 0.3
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
    
    
    def get_time_range(self):
        letter_array_list = self.extract_letters()     
        
        # Try Japanese parser first
        title = self.classifier_ja.predict(letter_array_list)
        
        r = re.findall(r'(\d{2}/\d{2}/\d{2})(\d{1,2}:\d{1,2}){0,1}', title)
        if len(r) >= 2: 
            def to_datetime(s):
                if s[1] == '':
                    return datetime.strptime(s[0], '%y/%m/%d')
                else:
                    return datetime.strptime(s[0] + ' ' + s[1], '%y/%m/%d %H:%M')
            out = [to_datetime(s) for s in r]
            return tuple(out)
        
        # if Japanese parser does not work, try English parser
        title = self.classifier_en.predict(letter_array_list)
        r = re.findall(r'([A-Za-z]{3})(\d{1,2}).(\d{4})', title)
        if len(r) >= 2:
            def to_datetime(s):
                return datetime.strptime(s[0] + ' ' + s[1] + ' ' + s[2], '%b %d %Y')
            out = [to_datetime(s) for s in r]
            return tuple(out)
        return ()
        
