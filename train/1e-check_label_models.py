
# coding: utf-8

# In[1]:

import os
import numpy as np
from glob import glob
from sklearn.externals import joblib

proj_root = os.path.abspath(os.path.join('../')) 
datadir = os.path.join(proj_root, 'data/labels/')
modeldir = os.path.join(proj_root, 'models/')


# In[2]:

X1 = np.load(os.path.join(datadir, 'X-1.npy'))
Y1 = np.load(os.path.join(datadir, 'Y-1.npy'))

X2 = np.load(os.path.join(datadir, 'X-2.npy'))
Y2 = np.load(os.path.join(datadir, 'Y-2.npy'))


X = np.vstack((X1, X2))
X_reshaped = X.reshape(X.shape[0], -1)
Y = np.concatenate((Y1, Y2))


# In[3]:

for fn in glob(os.path.join(modeldir, '*.pkl')):
    print(os.path.basename(fn), end='\n  accuracy = ')
    model = joblib.load(fn)
    print(model.score(X_reshaped, Y))


# In[ ]:




# In[ ]:



