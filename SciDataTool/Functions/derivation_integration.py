import numpy as np


def antiderivate():
    values = np.cumtrapz(values, x=axis_requested.values, axis=axis_requested.index)

    return values


def integrate(is_mean=True):
    values = np.trapz(values, x=axis_requested.values, axis=axis_requested.index)

    return values


def derivate(values, ax_val, ind, is_aper):
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

    if ax_val.size > 1:
        # Create the full vector of axis values
        ax_full = np.concatenate(
            (
                np.array([ax_val[0] - ax_val[1]]),
                ax_val,
                np.array([ax_val[-1] + ax_val[1] - ax_val[0]]),
            )
        )
        # Swap axis to always have derivating axis on 1st position
        shape = list(values.shape)
        values = np.swapaxes(values, ind, 0)
        shape[ind], shape[0] = shape[0], shape[ind]
        # Get values on a full (anti-)period
        shape[0] = shape[0] + 2
        values_full = np.zeros(shape, dtype=values.dtype)
        values_full[1:-1, ...] = values
        # Add first and last samples at the end and start of values to make values_full periodic
        # Last value is the same as (respectively the opposite of) the first value
        # in case of periodicity (respectively anti-periodicity)
        values_full[-1, ...] = (-1) ** int(is_aper) * values[0, ...]
        values_full[0, ...] = (-1) ** int(is_aper) * values[-1, ...]
        # Derivate along axis
        values = np.gradient(values_full, ax_full, axis=0)
        # Get N first values and swap axes back to origin
        values = np.swapaxes(values[1:-1, ...], 0, ind)

    else:
        raise Exception("Cannot derivate along axis if axis size is 1")

    return values
