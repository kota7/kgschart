# -*- coding: utf-8 -*- 


import os
import numpy as np
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline

from .utils import pad_crop_image 


class PadStackFlatten:
    def __init__(self, target_shape):
       if len(target_shape) != 2: 
           print('target shape must be length 2')
           raise
       self.target_shape = target_shape

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        out = [pad_crop_image(a, \
                              self.target_shape[0], \
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
          ('prep', PadStackFlatten(self.input_shape)),
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
        out = self.predictor.predict(X)
        out = ''.join(out)
        return out




class CaptionJaClassifier:
    predictor = None
    input_shape = (18, 11)
    modelfile = os.path.join(os.path.dirname(__file__), \
                             'models/caption-ja_model.pkl')

    conversions = {'2': ['z', 'Z'], 
                   '5': ['s', 'S'], 
                   '9': ['g'], 
                   '0': ['o', 'O'], 
                   '1': ['I', 'i', 'l']} 
    def __init__(self):
        model = joblib.load(self.modelfile)

        self.predictor = Pipeline([
          ('prep', PadStackFlatten(self.input_shape)),
          ('predict', model)
        ])
    
    def predict(self, X):
        """
        Return predicted date letters

        Args
          X: list of 2d-arrays of shape (nrow, ncol)

        Returns
          string of predicted date time expression
          YY/MM/DD HH:MM
        """
        if type(X) != list: X = [X]
        out = self.predictor.predict(X)
        for i in range(len(X)):
            if X[i].shape[0] > self.input_shape[0] or \
               X[i].shape[1] > self.input_shape[1]:
                   out[i] = ' '
        out = ''.join(out)

        for key in self.conversions:
            for letter in self.conversions[key]:
                out = out.replace(letter, key)
        return out
         

    

class CaptionEnClassifier:
    predictor = None
    modelfile_paren = os.path.join(os.path.dirname(__file__), \
            'models/caption-en-paren_model.pkl') 
    input_shape_paren = (18, 16)
    modelfile_letter = os.path.join(os.path.dirname(__file__), \
            'models/caption-en-letter_model.pkl')    
    input_shape_letter = (18, 18)

    conversions = {'Jul': ['JuI']}
    def __init__(self):
        model_paren = joblib.load(self.modelfile_paren)
        model_letter = joblib.load(self.modelfile_letter)
    
        self.predictor_paren = Pipeline([
          ('prep', PadStackFlatten(self.input_shape_paren)),
          ('predict', model_paren)
        ])
        self.predictor_letter = Pipeline([
          ('prep', PadStackFlatten(self.input_shape_letter)),
          ('predict', model_letter)
        ])

    def predict(self, X):
        if type(X) != list: X = [X]
        
        # find parenthesis
        y = self.predictor_paren.predict(X)
        for i in range(len(y)):
            if y[i] == '(':
                i1 = i
                break
        else:
            return ()
        for i in reversed(range(len(y))):
            if y[i] == ')':
                i2 = i
                break
        else:
            return()
        if i1 > i2: return ()
        
        # identify letters
        out = self.predictor_letter.predict(X[i1:i2])
        out = ''.join(out)
        for key in self.conversions:
            for letter in self.conversions[key]:
                out = out.replace(letter, key)
        return out


