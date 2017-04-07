#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import sys
import os
from glob import glob
from matplotlib import pyplot as plt
import numpy as np

# include kgschart directory to the python path
proj_root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
module_path = os.path.join(proj_root, 'kgschart')
sys.path.append(module_path)
from kgschart import KgsChart
from utils import pad_image


def remove_duplicates(arr):
    """
    # http://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array
    # Greg von Winckel
    """
    # first, flatten so that rows can be convert to tuples
    original_shape = arr.shape
    arr = arr.reshape(arr.shape[0], -1)
    # remove duplicate using hashing
    arr = np.vstack({tuple(row) for row in arr})
    # back to original shape
    new_shape = list(original_shape)
    new_shape[0] = arr.shape[0]
    arr = arr.reshape(new_shape)
    return arr



def save_x(filelist, outname, target_shape=None):
    # extract label letters from each image file
    letters = []
    for f in filelist:
        print(os.path.basename(f), '...')
        k = KgsChart(f)
        tmp = k.extract_caption_letters()
        letters += tmp
        
        #for l in letters:
        #    plt.imshow(l, cmap='gray')
        #    plt.show()
                    
    # max size of images
    maxi = 0
    maxj = 0
    for l in letters:
        maxi = max(maxi, l.shape[0])
        maxj = max(maxj, l.shape[1])
    print('max size = ', maxi, maxj)
    if target_shape is None:
        target_nrow = maxi + 4
        target_ncol = maxj + 4
    else:
        target_nrow = target_shape[0]
        target_ncol = target_shape[1]
    
    out = []
    for l in letters:
        if l.shape[0] > target_nrow or l.shape[1] > target_ncol:
            continue
        padded = pad_image(l, target_nrow, target_ncol, 1.0)
        out.append(padded)
        #plt.subplot(121)
        #plt.imshow(l, cmap='gray')
        #plt.subplot(122)
        #plt.imshow(padded, cmap='gray')
        #plt.show() 
    
    out = [o.reshape(1, o.shape[0], o.shape[1]) for o in out]
    out = np.vstack(out)
    print('output shape (with dup) = ', out.shape)
    
    # remove duplicate, save input time
    out = remove_duplicates(out)
    print('output shape (w/o dup)  = ', out.shape)
    

    out_dir = os.path.dirname(outname)
    if not os.path.isdir(out_dir): os.makedirs(out_dir)
    np.save(outname, out)
    print(outname, 'saved.\nDONE')


# data path
filelist = [f for f in glob(os.path.join(proj_root, 'data/images/batch1/*.png'))] + \
           [f for f in glob(os.path.join(proj_root, 'data/images/batch2/*.png'))]
save_x(filelist, os.path.join(proj_root, 'data/caption/X-ja.npy'), (17, 14))


