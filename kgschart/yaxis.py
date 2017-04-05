# -*- coding: utf-8 -*- 



class Yaxis:
    image = None
    nlabels = None

    def __init__(self, image):
        self.image = image
    

    def get_label_range(self):
        """
        Returns the min and max of y-axis labels

        Returns
          tuple of strings such as (2k, 1d)
        """
        return () 


    def get_label_data(self):
        """
        make Y-axis labal data

        Returns
            list of 3d-arrays X, where
            X[i, r, c] is the gray scale of cell (r,c) of i-th label
        """
        pass




