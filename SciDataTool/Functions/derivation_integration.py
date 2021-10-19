import numpy as np

from SciDataTool.Functions import AxisError


def antiderivate():
    values = np.cumtrapz(values, x=axis_requested.values, axis=axis_requested.index)

    return values


def integrate(values, ax_val, index, Nper, is_aper, is_phys):
    """Returns the integral of values along given axis

    Parameters
    ----------
    values: ndarray
        array to derivate
    ax_val: ndarray
        axis values
    index: int
        index of axis along which to derivate
    Nper: int
        number of periods to replicate
    is_aper: bool
        True if values is anti-periodic along axis
    is_phys: bool
        True if physical quantity (time/angle/z)

    Returns
    -------
    values: ndarray
        integral of values
    """
    if not is_phys:
        raise AxisError("Integration only available for time/angle/z")
    else:
        values = np.trapz(values, x=ax_val, axis=index)
        if is_aper:
            values = values - values
            Nper = int(Nper / 2)
        values *= Nper

    return values


def derivate(values, ax_val, index, Nper, is_aper, is_phys, is_freqs):
    """Returns the integral of values along given axis

    Parameters
    ----------
    values: ndarray
        array to derivate
    ax_val: ndarray
        axis values
    index: int
        index of axis along which to derivate
    Nper: int
        number of periods to replicate
    is_aper: bool
        True if values is anti-periodic along axis
    is_phys: bool
        True if physical quantity (time/angle/z)
    is_freqs: bool
        True if frequency axis

    Returns
    -------
    values: ndarray
        derivate of values
    """

    if is_freqs:
        dim_array = np.ones((1, values.ndim), int).ravel()
        dim_array[index] = -1
        axis_reshaped = ax_val.reshape(dim_array)
        values = values * axis_reshaped * 2 * 1j * np.pi

    elif is_phys:
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
            values = np.swapaxes(values, index, 0)
            shape[index], shape[0] = shape[0], shape[index]
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
            values = np.swapaxes(values[1:-1, ...], 0, index)

        else:
            raise Exception("Cannot derivate along axis if axis size is 1")
    else:
        raise AxisError("Derivation only available for time/angle/z/freqs")

    return values
