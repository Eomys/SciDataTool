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
    interp,
    where,
    zeros
)
from scipy.interpolate import interp1d


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
                initial = values1[argmin(np_abs([i - initial for i in values1])) + 1]
            if final not in values1:
                final = values1[argmin(np_abs([i - final for i in values1])) - 1]
        else:
            number = length2
            if initial not in values2:
                initial = values2[argmin(np_abs([i - initial for i in values2])) + 1]
            if final not in values2:
                final = values2[argmin(np_abs([i - final for i in values2])) - 1]
    return linspace(initial, final, int(number), endpoint=True)


def get_interpolation(values, axis_values, new_axis_values, index):
    """Returns the interpolated field along one axis, given the new axis
    Parameters
    ----------
    values: ndarray
        1Darray of a field along one axis
    axis_values: list
        values of the original axis
    new_axis_values: list
        values of the new axis
    index : int
        index of the axis
    Returns
    -------
    ndarray of the interpolated field
    """
    if str(axis_values) == "whole":  # Whole axis -> no interpolation
        return values
    elif len(new_axis_values) == 1:  # Single point -> use argmin
        idx = argmin(np_abs(axis_values - new_axis_values[0]))
        return take(values, [idx], axis=index)
    elif len(axis_values) == len(new_axis_values) and all(
        isclose(axis_values, new_axis_values, rtol=1e-03)
    ):  # Same axes -> no interpolation
        return values
    elif isin(
        new_axis_values, axis_values
    ).all():  # New axis is subset -> no interpolation

        indice_take = where(isin(axis_values, new_axis_values))[0]

        return take(
            values,
            indice_take,
            axis=index,
        )

    else:
        f = interp1d(axis_values, values, axis=index, fill_value="extrapolate")
        return f(new_axis_values)


def get_interpolation_step(values, axis_values, new_axis_values, index):
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
    # elif len(new_axis_values) == 1:  # Single point -> use argmin
    #     idx = argmin(np_abs(axis_values - new_axis_values[0]))
    #     return take(values, [idx])
    elif len(axis_values) == len(new_axis_values) and all(
        isclose(axis_values, new_axis_values, rtol=1e-03)
    ):  # Same axes -> no interpolation
        return values
    elif isin(
        new_axis_values, axis_values
    ).all():  # New axis is subset -> no interpolation
        indice_take = where(isin(axis_values, new_axis_values))[0]

        return take(
            values,
            indice_take,
            axis=index,
        )
    
    
        # return values[isin(axis_values, new_axis_values)]
    else:
        if len(axis_values) == 1:
            return array([take(values, 0, axis=index) for i in range(len(new_axis_values))])
        else:
            new_shape = list(values.shape)
            new_shape[index] = len(new_axis_values)
            new_values = zeros(tuple(new_shape))
            for i in range(len(new_axis_values)):
                for j in range(len(axis_values) - 1):
                    if (
                        new_axis_values[i] == axis_values[j]
                        and new_axis_values[i] == axis_values[j + 1]
                    ):
                        new_values[(slice(None),) * index + (i,)] = (take(values, j, axis=index) + take(values, j+1, axis=index)) / 2
                        # new_values.append((take(values, j, axis=index) + take(values, j+1, axis=index)) / 2)
                        break
                    elif (
                        new_axis_values[i] >= axis_values[j]
                        and new_axis_values[i] < axis_values[j + 1]
                    ):
                        new_values[(slice(None),) * index + (i,)] = take(values, j, axis=index)
                        # new_values.append(take(values, j, axis=index))
                        break
                    elif (
                        j == len(axis_values) - 2
                        and new_axis_values[i] == axis_values[j + 1]
                    ):
                        new_values[(slice(None),) * index + (i,)] = take(values, j+1, axis=index)
                        # new_values.append(take(values, j+1, axis=index))
                        break
            return array(new_values)
