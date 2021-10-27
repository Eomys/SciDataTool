import numpy as np

from SciDataTool.Functions.derivation_integration import integrate
from SciDataTool.Functions.conversions import convert


def my_sum(values, index, Nper, is_aper, unit):
    """Returns the arithmetic sum of values along given axis

    Parameters
    ----------
    values: ndarray
        array to derivate
    index: int
        index of axis along which to derivate
    Nper: int
        number of periods to replicate
    is_aper: bool
        True if values is anti-periodic along axis

    Returns
    -------
    values: ndarray
        arithmetic sum of values
    """

    if is_aper:
        # Sum of anti-periodic signal yields zero
        shape = list(values.shape)
        shape0 = [s for ii, s in enumerate(shape) if ii != index]
        values = np.zeros(shape0, dtype=values.dtype)
    else:
        # To sum dB or dBA
        if "dB" in unit:
            values = 10 * np.log10(
                np.sum(10 ** (values / 10), axis=index, keepdims=True)
            )
        else:
            # Take sum value multiplied by periodicity
            if Nper is None:
                # Set Nper to 1 in case of non-periodic axis
                Nper = 1
            values = Nper * np.sum(values, axis=index, keepdims=True)

    return values


def my_mean(values, ax_val, index, Nper, is_aper, is_phys):
    """Returns the mean (arithmetic or integral) of values along given axis

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
        mean of values
    """

    if ax_val.size == 1:  # Do not use integrate for single point axes
        is_phys = False

    if is_phys:
        # Integrate values and take mean value by dividing by integration interval in integrate()
        values = integrate(values, ax_val, index, Nper, is_aper, is_phys, is_mean=True)
    else:
        if is_aper:
            # Average of anti-periodic signal yields zero
            shape = list(values.shape)
            shape0 = [s for ii, s in enumerate(shape) if ii != index]
            values = np.zeros(shape0, dtype=values.dtype)
        else:
            # Take mean value multiplied by periodicity
            if Nper is None:
                # Set Nper to 1 in case of non-periodic axis
                Nper = 1
            values = Nper * np.mean(values, axis=index)

    return values


def root_mean_square(values, ax_val, index, Nper, is_aper, is_phys):
    """Returns the root mean square (arithmetic or integral) of values along given axis

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
        root mean square of values
    """

    if is_aper and Nper is not None:
        # Remove anti-periodicity since values is squared
        is_aper = False

    return np.sqrt(my_mean(values ** 2, ax_val, index, Nper, is_aper, is_phys))


def root_sum_square(values, ax_val, index, Nper, is_aper, is_phys, unit):
    """Returns the root sum square (arithmetic or integral) of values along given axis

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
        root sum square of values
    """

    # To sum dB or dBA
    if "dB" in unit:
        return my_sum(values, index, Nper, is_aper, unit)

    else:
        if is_aper and Nper is not None:
            # Remove anti-periodicity since values is squared
            is_aper = False

        if ax_val.size == 1:  # Do not use integrate for single point axes
            is_phys = False

        if is_phys:
            values = integrate(values ** 2, ax_val, index, Nper, is_aper, is_phys)
        else:
            values = my_sum(values ** 2, index, Nper, is_aper, unit)

        return np.sqrt(values)
