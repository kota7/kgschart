#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys
import numpy as np
from matplotlib import pyplot as plt


proj_root = os.path.abspath(os.path.join(os.path.dirname( \
    os.path.realpath(__file__)), '../'))


def input_y(xfile, yfile, resume=True):
    X = np.load(xfile)
    if os.path.isfile(yfile) and resume:
        Y = np.load(yfile)
    else:
        Y = [''] * X.shape[0]
        
    i = 0
    plt.plot(1)
    plt.show(block = False)
    while i < int(X.shape[0]):
        # skip if y value is already given
        if len(Y[i]) != 0: 
            i += 1
            continue
        
        print(i+1, '/', X.shape[0])
        im = X[i]
        plt.imshow(im, cmap = 'gray')
        plt.draw()
        while True:
            ans = input('what is this? >')
            break
        if ans == 'back':
            i -= 1
        elif ans in ['break', 'exit']:
            break
        else:
            Y[i] = ans
            i += 1  
                  
    np.save(yfile, Y)
    print(yfile, 'saved\nDone')



datadir = os.path.join(proj_root, 'data/caption/')
input_y(os.path.join(datadir, 'X-ja.npy'), os.path.join(datadir, 'Y-ja.npy'))
