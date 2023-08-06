# coding: utf-8

"""
Automated Tool for Optimized Modelling (ATOM)
Author: tvdboom
Description: Utility variables for the tests.

"""

# Import packages
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import (
    load_breast_cancer, load_wine,  load_digits, load_diabetes
    )


# Functions ================================================================= >>

def merge(X, y):
    """Merge a pd.DataFrame and pd.Series into one dataframe."""
    return X.merge(y.to_frame(), left_index=True, right_index=True)


# Variables ================================================================= >>

# Directory for storing all files created by the tests
FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'

# Sklearn datasets for all three tasks as np.array
X_bin_array, y_bin_array = load_breast_cancer(return_X_y=True)
X_class_array, y_class_array = load_digits(return_X_y=True)
X_reg_array, y_reg_array = load_diabetes(return_X_y=True)

# Sklearn datasets for all three tasks as pd.DataFrame
X_bin, y_bin = load_breast_cancer(return_X_y=True, as_frame=True)
X_class, y_class = load_wine(return_X_y=True, as_frame=True)
X_class2, y_class2 = load_digits(return_X_y=True, as_frame=True)
X_reg, y_reg = load_diabetes(return_X_y=True, as_frame=True)

# Train and test sets for all three tasks
bin_train, bin_test = train_test_split(merge(X_bin, y_bin), test_size=0.3)
class_train, class_test = train_test_split(merge(X_class, y_class), test_size=0.3)
reg_train, reg_test = train_test_split(merge(X_reg, y_reg), test_size=0.3)

# Small dimensional dataset
X10 = [[0.2, 2, 1], [0.2, 2, 1], [0.2, 2, 2], [0.24, 2, 1], [0.23, 2, 2],
       [0.19, 0, 1], [0.21, 3, 2], [0.2, 2, 1], [0.2, 2, 1], [0.2, 2, 0]]
X10_nan = [[np.NaN, 2, 1], [0.2, 2, 1], [4, 2, 2], [3, 2, 1], [3, 2, 2],
           [1, 0, 1], [0, 3, 2], [4, 2, 1], [5, 2, 1], [3, 2, 0]]
X10_str = [[2, 0, 'a'], [2, 3, 'a'], [5, 2, 'b'], [1, 2, 'a'], [1, 2, 'c'],
           [2, 0, 'd'], [2, 3, 'd'], [5, 2, 'd'], [1, 2, 'a'], [1, 2, 'd']]
X10_str2 = [[2, 0, 'a'], [2, 3, 'a'], [5, 2, 'b'], [1, 2, 'a'], [1, 2, 'a'],
            [2, 0, 'a'], [2, 3, 'b'], [5, 2, 'b'], [1, 2, 'a'], [1, 2, 'a']]
X10_sn = [[2, 0, np.NaN], [2, 3, 'a'], [5, 2, 'b'], [1, 2, 'a'], [1, 2, 'c'],
          [2, 0, 'd'], [2, 3, 'd'], [5, 2, 'd'], [1, 2, 'a'], [1, 2, 'd']]
y10 = [0, 1, 0, 1, 1, 0, 1, 0, 1, 1]
y10_str = ['y', 'n', 'y', 'y', 'n', 'y', 'n', 'y', 'n', 'n']
