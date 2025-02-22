#/usr/bin/env python3
####################################################################################
#   Copyright (c) 2025
#
#   Team: System of a Down
#
#   Authors: Freddie Fraticelli, John Midkiff, Zack Popilek,
#            Ashley Porter, and Gerardo Rivas-Leal
#   
#   
#   This project is open source and can be utilized and referenced
#   as long as the team and all authors are credited.
#
#
#
####################################################################################

import numpy as np
from math import isclose
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from math import e
import statsmodels.api as sm

class DataStorage:

    def fit_exponential_equation(self, x, y, c):
        """
        Fits the equation c = x^a * y^b to the given data.

        Args:
            x: Array of x values.
            y: Array of y values.
            c: Array of c values.

        Returns:
            A tuple containing the fitted values of a and b.
        """

        C = np.log(c)
        X = np.column_stack([x, y])

        model = LinearRegression()
        model.fit(X, C)

        a = np.exp(model.coef_[0])
        b = np.exp(model.coef_[1])

        return a, b
    
    def get_C(self, a, b , x , y):
        """
         c = x^a * y^b
        """
        return (x**a) * (y**b)