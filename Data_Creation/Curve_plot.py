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
    def __init__(self, data):
        self.points = np.array(data)

    def get_X_and_Y_vec(self):
        return self.points[:, 0], self.points[:, 1]
    
    def cal_poly(self):
        z = self.get_poly_fit()
        return np.poly1d(z)
    
    def get_poly_fit(self):
        x,y = self.get_X_and_Y_vec()
        return np.polyfit(x, y, self.degree)

    def get_new_x_and_y(self):
        x,y = self.get_X_and_Y_vec()
        f = self.cal_poly()

        x_new = np.linspace(x[0], x[-1])
        y_new = f(x_new) 
        return x_new, y_new
    
    # Polynomial Regression
    def r_squared(self, degree):
        x,y = self.get_X_and_Y_vec()
        results = {}

        coeffs = np.polyfit(x, y, degree)
        # Polynomial Coefficients
        results['polynomial'] = coeffs.tolist()

        correlation = np.corrcoef(x, y)[0,1]

        # r
        results['correlation'] = correlation
        # r-squared
        results['determination'] = correlation**2

        return results

    def find_degree_order(self):
        r_sq = 0.0
        degree = 0
        while(isclose(r_sq, 0.95, rel_tol=1)):
            r_sq = self.r_squared(degree)
            degree += 1
        
        self.degree = degree
    
    def plot_data(self, show = False, save_im = False, image_dir="",  image_name = ""):

        # Get x and y as well as the new x and y values
        x, y = self.get_X_and_Y_vec()
        x_new, y_new  = self.get_new_x_and_y()

        #Plot the data
        plt.plot(x, y, 'o' , x_new, y_new)

        # Do we want to save the plots
        if save_im:
            dir_and_loc = image_dir + image_name
            plt.savefig(dir_and_loc, bbox_inches='tight')
        if show:
            plt.tight_layout()
            # plt.xticks(x)
            plt.show()

    
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