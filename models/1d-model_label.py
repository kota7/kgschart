#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split



proj_root = os.path.abspath(os.path.join(os.path.dirname( \
    os.path.realpath(__file__)), '../')) 
datadir = os.path.join(proj_root, 'data/labels/')


X = np.load(os.path.join(datadir, 'X.npy'))
Y = np.load(os.path.join(datadir, 'Y.npy'))


X_train, X_test, Y_train, Y_test  = train_test_split(
        X, Y, test_size = 0.25, stratify = Y)

pd.Series(Y_train).value_counts()


