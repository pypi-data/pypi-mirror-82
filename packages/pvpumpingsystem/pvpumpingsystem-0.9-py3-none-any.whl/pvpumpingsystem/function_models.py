# -*- coding: utf-8 -*-
"""
Module gathering mathematical function, including typical function templates.

@author: Tanguy Lunel
"""
import numpy as np
from sklearn.metrics import r2_score


def correlation_stats(funct_mod, params, data_input, data_to_fit):
    """
    Compute statistical figures to assess quality of curve fitting.
    In particular 'root mean square error', 'normalized root mean square
    error', 'r_squared', 'adjusted_r_squared' and size of data
    sample 'nb_data' are computed.

    Returns
    -------
    dict
        Keys are:
        -'rmse'
        -'nrmse'
        -'r_squared'
        -'adjusted_r_squared'
        -'nb_data'
    """
    data_fitted = funct_mod(data_input, *params)
    rmse = np.sqrt(sum((data_to_fit-data_fitted)**2)/len(data_to_fit))
    nrmse = rmse/np.mean(data_fitted)
    r_squared = r2_score(data_to_fit, data_fitted)

    nb_data = len(data_to_fit)
    nb_independent_variables = len(data_input)
    adjusted_r_squared = 1 - (1 - r_squared) * \
        ((nb_data - 1) / (nb_data - nb_independent_variables - 1))

    return {'rmse': rmse,
            'nrmse': nrmse,
            'r_squared': r_squared,
            'adjusted_r_squared': adjusted_r_squared,
            'nb_data': nb_data}


def compound_polynomial_1_2(input_val, a1, a2, a3, b1, b2, b3):
    """
    Model of a compound polynomial function made of a global equation of
    first order on x, for which each coefficient follows a second order
    equation on y.
    """
    x, y = input_val[0], input_val[1]
    a = polynomial_2(y, a1, a2, a3)
    b = polynomial_2(y, b1, b2, b3)
    return a + b*x


def compound_polynomial_1_3(input_val, a1, a2, a3, a4, b1, b2, b3, b4):
    """
    Model of a compound polynomial function made of a global equation of
    first order on x, for which each coefficient follows a third order
    equation on y.
    """
    x, y = input_val[0], input_val[1]
    a = polynomial_3(y, a1, a2, a3, a4)
    b = polynomial_3(y, b1, b2, b3, b4)
    return a + b*x


def compound_polynomial_2_2(input_val, a1, a2, a3, b1, b2, b3, c1, c2, c3):
    """
    Model of a compound polynomial function made of a global equation of
    second order on x, for which each coefficient follows a third order
    equation on y.
    """
    x, y = input_val[0], input_val[1]
    a = polynomial_2(y, a1, a2, a3)
    b = polynomial_2(y, b1, b2, b3)
    c = polynomial_2(y, c1, c2, c3)
    return a + b*x + c*x**2


def compound_polynomial_2_3(input_val, a1, a2, a3, a4, b1, b2, b3, b4,
                            c1, c2, c3, c4):
    """
    Model of a compound polynomial function made of a global equation of
    second order on x, for which each coefficient follows a third order
    equation on y.
    """
    x, y = input_val[0], input_val[1]
    a = polynomial_3(y, a1, a2, a3, a4)
    b = polynomial_3(y, b1, b2, b3, b4)
    c = polynomial_3(y, c1, c2, c3, c4)
    return a + b*x + c*x**2


def compound_polynomial_3_3(input_val, a1, a2, a3, a4, b1, b2, b3, b4,
                            c1, c2, c3, c4, d1, d2, d3, d4):
    """
    Model of a compound polynomial function made of a global equation of
    third order on x, for which each coefficient follows a third order
    equation on y.
    """
    x, y = input_val[0], input_val[1]
    a = polynomial_3(y, a1, a2, a3, a4)
    b = polynomial_3(y, b1, b2, b3, b4)
    c = polynomial_3(y, c1, c2, c3, c4)
    d = polynomial_3(y, d1, d2, d3, d4)
    return a + b*x + c*x**2 + d*x**3


def polynomial_multivar_3_3_4(input_val, y_intercept, a1, a2, a3, b1, b2, b3,
                              c1, c2, c3, c4):
    """
    Model of a multivariate polynomial function of third order on x and y,
    and with 1 interaction term.
    """
    x, y = input_val[0], input_val[1]
    return y_intercept + a1*x + a2*x**2 + a3*x**3 \
        + b1*y + b2*y**2 + b3*y**3 \
        + c1*x*y + c2*x**2*y + c3*x*y**2 + c4*x**2*y**2


def polynomial_multivar_3_3_1(input_val, y_intercept, a1, a2, a3, b1, b2, b3,
                              c1):
    """
    Model of a multivariate polynomial function of third order on x and y,
    and with 1 interaction term.
    """
    x, y = input_val[0], input_val[1]
    return y_intercept + a1*x + a2*x**2 + a3*x**3 + \
        b1*y + b2*y**2 + b3*y**3 + c1*x*y


def polynomial_multivar_2_2_1(input_val, y_intercept, a1, a2, b1, b2, c1):
    """
    Model of a multivariate polynomial function of second order on x and y,
    and with 1 interaction term.
    """
    x, y = input_val[0], input_val[1]
    return y_intercept + a1*x + a2*x**2 + b1*y + b2*y**2 + c1*x*y


def polynomial_multivar_2_2_0(input_val, y_intercept, a1, a2, b1, b2):
    """
    Model of a multivariate polynomial function of second order on x and y,
    and with no interaction term.
    """
    x, y = input_val[0], input_val[1]
    return y_intercept + a1*x + a2*x**2 + b1*y + b2*y**2


def polynomial_multivar_1_1_0(input_val, y_intercept, a1, b1):
    """
    Model of a multivariate polynomial function of first order on x and y,
    and with no interaction term.
    """
    x, y = input_val[0], input_val[1]
    return y_intercept + a1*x + b1*y


def polynomial_multivar_0_1_0(input_val, y_intercept, b1):
    """
    Model of a multivariate polynomial function of first order on y
    (actually not really multivariate so).
    """
    x, y = input_val[0], input_val[1]
    return y_intercept + 0*x + b1*y


def polynomial_5(x, y_intercept, a, b, c, d, e):
    """
    Model of a polynomial function of fifth order.
    """
    return y_intercept + a*x + b*x**2 + c*x**3 + d*x**4 + e*x**5


def polynomial_4(x, y_intercept, a, b, c, d):
    """
    Model of a polynomial function of fourth order.
    """
    return y_intercept + a*x + b*x**2 + c*x**3 + d*x**4


def polynomial_3(x, y_intercept, a, b, c):
    """
    Model of a polynomial function of third order.
    """
    return y_intercept + a*x + b*x**2 + c*x**3


def polynomial_2(x, y_intercept, a, b):
    """
    Model of a polynomial function of second order.
    """
    return y_intercept + a*x + b*x**2


def polynomial_1(x, y_intercept, a):
    """
    Model of a polynomial function of first order, i.e. a linear function.
    """
    return y_intercept + a*x


def polynomial_divided_2_1(x, a, b, c):
    """
    Model of a polynomial function of second order divided by x.
    """
    return a/x + b + c*x
