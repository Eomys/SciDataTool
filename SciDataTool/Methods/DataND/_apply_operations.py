from numpy import abs as np_abs

from SciDataTool.Functions.derivation_integration import (
    derivate,
    integrate,
    integrate_local,
    antiderivate,
)
from SciDataTool.Functions.sum_mean import (
    my_sum,
    my_mean,
    root_mean_square,
    root_sum_square,
)


def _apply_operations(self, values, axes_list, is_magnitude, unit):
    """Returns the values of the field transformed or converted
    Parameters
    ----------
    self: Data
        a Data object
    values: ndarray
        array of the field
    Returns
    -------
    values: ndarray
        values of the field
    """

    # Take magnitude before summing
    if is_magnitude and "dB" not in unit:
        values = np_abs(values)

    # Apply sums, means, etc
    for axis_requested in axes_list:
        # Get axis data
        ax_val = axis_requested.values
        extension = axis_requested.extension
        index = axis_requested.index
        if axis_requested.is_pattern:
            Nper, is_aper = None, None
        else:
            Nper, is_aper = self.axes[index].get_periodicity()
        if axis_requested.name in ["time", "angle", "z"]:
            is_phys = True
            is_freqs = False
        elif axis_requested.name in ["freqs", "frequency"]:
            is_phys = False
            is_freqs = True
        else:
            is_phys = False
            is_freqs = False
        # sum over sum axes
        if extension in "sum":
            values = my_sum(values, index, Nper, is_aper, unit)
        # root sum square over rss axes
        elif extension == "rss":
            values = root_sum_square(
                values, ax_val, index, Nper, is_aper, is_phys, unit
            )
        # mean value over mean axes
        elif extension == "mean":
            values = my_mean(values, ax_val, index, Nper, is_aper, is_phys)
        # RMS over rms axes
        elif extension == "rms":
            values = root_mean_square(values, ax_val, index, Nper, is_aper, is_phys)
        # integration over integration axes
        elif extension == "integrate":
            values = integrate(values, ax_val, index, Nper, is_aper, is_phys)
        # local integration over integration axes
        elif extension == "integrate_local":
            values = integrate_local(
                values, ax_val, index, Nper, is_aper, is_phys, is_freqs
            )
        # antiderivation over antiderivation axes
        elif extension == "antiderivate":
            values = antiderivate(
                values, ax_val, index, Nper, is_aper, is_phys, is_freqs
            )
        # derivation over derivation axes
        elif extension == "derivate":
            values = derivate(values, ax_val, index, Nper, is_aper, is_phys, is_freqs)

    if is_magnitude and "dB" in unit:  # Correction for negative/small dB/dBA
        values[values < 2] = 0
        values = np_abs(values)

    return values
