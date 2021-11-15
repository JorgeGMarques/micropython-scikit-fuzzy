"""
_normalize_columns.py : Normalize columns.
"""
from ulab import numpy as np


def normalize_columns(columns):
    """
    Normalize columns of matrix.

    Parameters
    ----------
    columns : 2d array (M x N)
        Matrix with columns

    Returns
    -------
    normalized_columns : 2d array (M x N)
        columns/np.sum(columns, axis=0)
    """

    # broadcast sum over columns
    normalized_columns = columns/np.sum(columns, axis=0)

    return normalized_columns


def normalize_power_columns(x, exponent):
    """
    Calculate normalize_columns(x**exponent)
    in a numerically safe manner.

    Parameters
    ----------
    x : 2d array (M x N)
        Matrix with columns
    n : float
        Exponent

    Returns
    -------
    result : 2d array (M x N)
        normalize_columns(x**n) but safe

    """

    # assert np.all(x >= 0.0) ::CANT::

    # x = x.astype(np.float64) ::CANT::

    # values in range [0, 1]
    x = x/np.max(x, axis=0)


    if exponent < 0:
        # values in range [1, 1/eps]
        x /= np.min(x, axis=0)

        # values in range [1, (1/eps)**exponent] where exponent < 0
        # this line might trigger an underflow warning
        # if (1/eps)**exponent becomes zero, but that's ok
        x = x**exponent
    else:
        # values in range [eps**exponent, 1] where exponent >= 0
        x = x**exponent

    result = normalize_columns(x)

    return result
