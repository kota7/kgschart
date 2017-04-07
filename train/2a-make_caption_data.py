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



def save_x(data_dir, suffix, out_dir, 
           target_nrow=16, target_ncol=12):
    # extract label letters from each image file
    letters = []
    for f in glob(os.path.join(data_dir, '*.png')):
        print(os.path.basename(f), '...')
        k = KgsChart(f)
        tmp = k.extract_caption_letters()
        letters += tmp
    
    # remove all letters target col size
    letters = list(filter(lambda l: l.shape[1] <= target_ncol, letters))
    
    # max size of images
    maxi = 0
    maxj = 0
    for l in letters:
        maxi = max(maxi, l.shape[0])
        maxj = max(maxj, l.shape[1])
    print('max size = ', maxi, maxj)
    #target_nrow = maxi + 4
    #target_ncol = maxj + 4
    
    out = []
    for l in letters:
        padded = pad_image(l, target_nrow, target_ncol, 1.0)
        out.append(padded)
        #plt.subplot(121)
        #plt.imshow(l, cmap='gray')
        #plt.subplot(122)
        #plt.imshow(padded, cmap='gray')
        #plt.show() 
    
    out = [o.reshape(1, o.shape[0], o.shape[1]) for o in out]
    out = np.vstack(out)


    if not os.path.isdir(out_dir): os.makedirs(out_dir)
    outname = os.path.join(out_dir, 'X%s.npy' % suffix)
    np.save(outname, out)
    print(outname, 'saved.\nDONE')


# data path
save_x(os.path.join(proj_root, 'data/images/batch1'), '-1', 
       os.path.join(proj_root, 'data/caption'))
#save_x(os.path.join(proj_root, 'data/images/batch2'), '-2', 
#       os.path.join(proj_root, 'data/caption'))

