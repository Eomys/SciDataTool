import numpy as np


def sum():
    values = np.trapz(values, x=axis_requested.values, axis=axis_requested.index)

    return values


def mean(values, ax_val, ind, is_aper):
    """Returns the first derivate of values along given axis
    values is assumed to be periodic and axis is assumed to be a linspace

    Parameters
    ----------
    values: ndarray
        array to derivate
    ax_val: ndarray
        axis values
    ind: int
        index of axis along which to derivate
    is_aper: bool
        True if values is anti-periodic along axis

    Returns
    -------
    values: ndarray
        derivative of values
    """

    return values

def root_mean_square():

    return values

def root_sum_square():

    return values
