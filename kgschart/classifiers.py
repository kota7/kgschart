# -*- coding: utf-8 -*- 


import os
import numpy as np
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from pkg_resources import resource_stream

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



# load pretrained models here, 
# so all instances of a same class share a single model object
# no need to load models when a new instance is created.
model_dict = dict(
    label=(joblib.load(resource_stream(__name__, 'models/label_model.pkl')),
          (16, 12)),
          
    caption_ja=(joblib.load(resource_stream(__name__, 
                                            'models/caption-ja_model.pkl')),
               (18, 11)),
               
    caption_en_paren=(joblib.load(resource_stream(__name__, 
                                                  'models/caption-en-paren_model.pkl')),
                     (18, 16)),
    caption_en_letter=(joblib.load(resource_stream(__name__, 
                                                   'models/caption-en-letter_model.pkl')),
                      (18, 18))
)


class LabelClassifier:

    model, input_shape = model_dict['label']
    predictor = Pipeline([
        ('prep', PadStackFlatten(input_shape)),
        ('predict', model)
    ]) 
    
    def __init__(self):
        pass

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

    model,input_shape = model_dict['caption_ja']
    predictor = Pipeline([
        ('prep', PadStackFlatten(input_shape)),
        ('predict', model)
    ]) 
    
    conversions = {'2': ['z', 'Z'], 
                   '5': ['s', 'S'], 
                   '9': ['g'], 
                   '0': ['o', 'O'], 
                   '1': ['I', 'i', 'l']} 
    def __init__(self):
        pass
    
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

    model_paren, input_shape_paren = model_dict['caption_en_paren']
    predictor_paren = Pipeline([
        ('prep', PadStackFlatten(input_shape_paren)),
        ('predict', model_paren)
    ])
    
    model_letter, input_shape_letter = model_dict['caption_en_letter']
    predictor_letter = Pipeline([
        ('prep', PadStackFlatten(input_shape_letter)),
        ('predict', model_letter)
    ])

    conversions = {'Jul': ['JuI']}
    def __init__(self):
        pass

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


