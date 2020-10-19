# -*- coding: utf-8 -*-
from numpy import (
    array,
    linspace,
    argmin,
    take,
    isclose,
    isin,
    around,
    all,
    abs as np_abs,
)
from scipy import interpolate


def get_common_base(values1, values2, is_extrap=False, is_downsample=False):
    """Returns a common base for vectors values1 and values2
    Parameters
    ----------
    values1: list
        values of the first axis
    values2: list
        values of the second axis
    is_extrap: bool
        Boolean indicating if we want to keep the widest vector and extrapolate the other one
    is_downsample: bool
        Boolean indicating if we want to keep the smallest number of points and downsample the other one
    Returns
    -------
    list of the common axis values
    """
    # if len(values1) == 2:
    #     return array([x for x in values2 if x >= values1[0] and x <= values1[-1]])
    # else:
    if is_extrap:
        initial = min(values1[0], values2[0])
        final = max(values1[-1], values2[-1])
    else:
        initial = max(values1[0], values2[0])
        final = min(values1[-1], values2[-1])
    if is_downsample:
        number = min(
            len([i for i in values1 if i >= initial and i <= final]),
            len([i for i in values2 if i >= initial and i <= final]),
        )
    else:
        length1 = len([i for i in values1 if i >= initial and i <= final])
        length2 = len([i for i in values2 if i >= initial and i <= final])
        if length1 > length2:
            number = length1
            if initial not in values1:
                initial = values1[
                    argmin(np_abs([i - initial for i in values1])) + 1
                ]
            if final not in values1:
                final = values1[argmin(np_abs([i - final for i in values1])) - 1]
        else:
            number = length2
            if initial not in values2:
                initial = values2[
                    argmin(np_abs([i - initial for i in values2])) + 1
                ]
            if final not in values2:
                final = values2[argmin(np_abs([i - final for i in values2])) - 1]
    return linspace(initial, final, int(number), endpoint=True)


def get_interpolation(values, axis_values, new_axis_values):
    """Returns the interpolated field along one axis, given the new axis
    Parameters
    ----------
    values: ndarray
        1Darray of a field along one axis
    axis_values: list
        values of the original axis
    new_axis_values: list
        values of the new axis
    Returns
    -------
    ndarray of the interpolated field
    """
    if str(axis_values) == "whole":  # Whole axis -> no interpolation
        return values
    elif len(new_axis_values) == 1:  # Single point -> use argmin
        idx = argmin(np_abs(axis_values - new_axis_values[0]))
        return take(values, [idx])
    elif len(axis_values) == len(new_axis_values) and all(
        isclose(axis_values, new_axis_values, rtol=1e-03)
    ):  # Same axes -> no interpolation
        return values
    elif isin(
        around(new_axis_values, 5), around(axis_values, 5), assume_unique=True
    ).all():  # New axis is subset -> no interpolation
        return values[
            isin(around(axis_values, 5), around(new_axis_values, 5), assume_unique=True)
        ]
    else:
        f = interpolate.interp1d(axis_values, values)
        return f(new_axis_values)
