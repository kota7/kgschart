#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import sys
import os
from glob import glob
from matplotlib import pyplot as plt

# include kgschart directory to the python path
proj_root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
module_path = os.path.join(proj_root, 'kgschart')
sys.path.append(module_path)
from kgschart import KgsChart

# data path
data_dir = os.path.join(proj_root, 'data/images')

# extract label letters from each image file
letters = []
for f in glob(os.path.join(data_dir, '*.png')):
    k = KgsChart(f)
    tmp = k.extract_label_letters()
    for l in tmp:
        if (l.shape[0] > 20 or l.shape[1] > 20):
            print(f)
            plt.imshow(l, cmap='gray')
            plt.show()
            k.display()
        
    letters += tmp

# max size of images
for l in letters:
    print(l.shape)
    