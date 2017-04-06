#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys
import numpy as np
from matplotlib import pyplot as plt


proj_root = os.path.abspath(os.path.join(os.path.dirname( \
    os.path.realpath(__file__)), '../'))


def input_y(xfile):
    X = np.load(xfile)

    Y = np.chararray(int(X.shape[0])) 
    Y[:] = ''
    i = 0
    plt.plot(1)
    plt.show(block = False)
    while i < int(X.shape[0]):
        print(i+1, '/', X.shape[0])
        im = X[i]
        plt.imshow(im, cmap = 'gray')
        plt.draw()
        while True:
            ans = input('what is this? >')
            if (not ans == '') and (ans in '0123456789kdbe'):
                break
        if ans == 'b':
            i -= 1
        elif ans == 'e':
            return
        else:
            Y[i] = ans
            i += 1  
                  
    outname = os.path.join(os.path.dirname(xfile),
                           os.path.basename(xfile).replace('X', 'Y'))
    np.save(outname, Y)
    print(outname, 'saved\nDone')



datadir = os.path.join(proj_root, 'data/labels/')
#input_y(os.path.join(datadir, 'X-1.npy'))
input_y(os.path.join(datadir, 'X-2.npy'))
