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

# data path
data_dir = os.path.join(proj_root, 'data/images')

# extract label letters from each image file
letters = []
for f in glob(os.path.join(data_dir, '*.png')):
    k = KgsChart(f)
    tmp = k.extract_label_letters()
    letters += tmp

# max size of images
maxi = 0
maxj = 0
for l in letters:
    maxi = max(maxi, l.shape[0])
    maxj = max(maxj, l.shape[1])

# add extra 2 pixels each 
target_nrow = maxi + 4 
target_ncol = maxj + 4
out = []
for l in letters:
    padded = pad_image(l, target_nrow, target_ncol, 1.0)
    #plt.subplot(121)
    #plt.imshow(l, cmap='gray')
    #plt.subplot(122)
    #plt.imshow(padded, cmap='gray')
    #plt.show() 
    out.append(padded)

out = [o.reshape(1, o.shape[0], o.shape[1]) for o in out]
out = np.vstack(out)


outdir = os.path.join(proj_root, 'data/labels/')
if not os.path.isdir(outdir): os.makedirs(outdir)
np.save(os.path.join(outdir, 'X.npy'), out)




