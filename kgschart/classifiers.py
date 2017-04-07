# -*- coding: utf-8 -*- 


import os
import numpy as np
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline

from utils import pad_image



class PadAndFlatten:
    def __init__(self, target_shape):
       if len(target_shape) != 2: 
           print('target shape must be length 2')
           raise
       self.target_shape = target_shape

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        out = [pad_image(a, self.target_shape[0], 
                         self.target_shape[1], 1.0) \
               for a in X]
        out = np.expand_dims(out, axis=0)
        out = np.vstack(out) 
        out = out.reshape(out.shape[0], -1)
        return out



class LabelClassifier:
    # prediction pipeline object
    predictor = None

    # don't know best practice to implement model save/load
    modelfile = os.path.join(os.path.dirname(__file__),
                             'models/label_model.pkl')
    input_shape = (16, 12)

    def __init__(self):
        # load model
        model = joblib.load(self.modelfile)

        # predictor pipeline
        self.predictor = Pipeline([
          ('prep', PadAndFlatten(self.input_shape)),
          ('predict', model)
        ]) 


    def predict(self, X):
        """
        Return predicted rank label

        Args
          X: list of 2d-arrays of shape (nrow, ncol)

        Returns
          string of predicted rank, e.g. 2k, 5d
        """
        if type(X) != list: X = [X]
        for a in X: print(a.shape)
        return self.predictor.predict(X)



