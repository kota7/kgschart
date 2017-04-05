#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split



proj_root = os.path.abspath(os.path.join(os.path.dirname( \
    os.path.realpath(__file__)), '../')) 
datadir = os.path.join(proj_root, 'data/labels/')


X1 = np.load(os.path.join(datadir, 'X-1.npy'))
Y1 = np.load(os.path.join(datadir, 'Y-1.npy'))

X2 = np.load(os.path.join(datadir, 'X-2.npy'))
Y2 = np.load(os.path.join(datadir, 'Y-2.npy'))

print(X1.shape, X2.shape)
print(Y1.shape, Y2.shape)

X = np.vstack((X1, X2))
Y = np.concatenate((Y1, Y2))
print(X.shape)
print(Y.shape)

X_train, X_test, Y_train, Y_test  = train_test_split(
        X, Y, test_size = 0.25, stratify = Y)

print(pd.Series(Y_train).value_counts())
print(pd.Series(Y_test).value_counts())


