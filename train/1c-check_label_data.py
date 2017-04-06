#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from matplotlib import pyplot as plt
import numpy as np
import os



proj_root = os.path.abspath(os.path.join(os.path.dirname( \
    os.path.realpath(__file__)), '../'))


def check(xfile, yfile):
    X = np.load(xfile)
    Y = np.load(yfile)
    
    print('size of X =', len(X), '; size of Y =', len(Y))
    if len(X) != len(Y):
        print('length mismatch!')
        return
        
    index = np.random.permutation(len(X))
    i = 0
    while i < len(X): 
        for j in range(9):
            if i >= len(X): break
            a = plt.subplot(3, 3, j+1)
            a.set_title(Y[index[i]].decode('utf-8'))
            a.imshow(X[index[i]], cmap='gray')
            i += 1
        plt.show()
        
#check(os.path.join(proj_root, 'data/labels/X-1.npy'), \
#      os.path.join(proj_root, 'data/labels/Y-1.npy')) 
      
check(os.path.join(proj_root, 'data/labels/X-2.npy'), \
      os.path.join(proj_root, 'data/labels/Y-2.npy')) 
