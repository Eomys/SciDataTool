import numpy as np

from SciDataTool.Functions import NormError, UnitError, AxisError
from SciDataTool.Functions.conversions import convert as convert_unit, to_dB, to_dBA


def convert(self, values, unit, is_norm, is_squeeze, is_magnitude, axes_list):
    """Returns the values of the field transformed or converted.
    Parameters
    ----------
    self: Data
        a Data object
    values: ndarray
        array of the field
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    Returns
    -------
    values: ndarray
        values of the field
    """

    # Take magnitude before summing
    if is_magnitude:
        values = np.abs(values)

    # Apply sums, means, etc
    for axis_requested in axes_list:
        # sum over sum axes
        if axis_requested.extension == "sum":
            values = np.sum(values, axis=axis_requested.index, keepdims=True)
        # root sum square over rss axes
        elif axis_requested.extension == "rss":
            values = np.sqrt(
                np.sum(values ** 2, axis=axis_requested.index, keepdims=True)
            )
        # mean value over mean axes
        elif axis_requested.extension == "mean":
            values = np.mean(values, axis=axis_requested.index, keepdims=True)
        # RMS over rms axes
        elif axis_requested.extension == "rms":
            values = np.sqrt(
                np.mean(values ** 2, axis=axis_requested.index, keepdims=True)
            )
        # integration over integration axes
        elif axis_requested.extension == "integrate":
            if axis_requested.name == "freqs":
                dim_array = np.ones((1, values.ndim), int).ravel()
                dim_array[axis_requested.index] = -1
                axis_reshaped = axis_requested.values.reshape(dim_array)
                axis_reshaped[axis_reshaped == 0] = np.inf  # put f=0 component to 0
                values = values / (axis_reshaped * 2 * 1j * np.pi)
            else:
                values = np.trapz(
                    values, x=axis_requested.values, axis=axis_requested.index
                )
        # derivation over derivation axes
        elif axis_requested.extension == "derivate":
            if axis_requested.name == "freqs":
                dim_array = np.ones((1, values.ndim), int).ravel()
                dim_array[axis_requested.index] = -1
                axis_reshaped = axis_requested.values.reshape(dim_array)
                values = values * axis_reshaped * 2 * 1j * np.pi
            elif axis_requested.name in ["time", "angle"]:
                if axis_requested.values.size > 1:
                    # quantity is assumed to be periodic and axis is assumed to be a linspace
                    ind = axis_requested.index
                    _, is_aper = self.axes[ind].get_periodicity()
                    shape = list(values.shape)
                    # Create the full vector of axis values
                    ax_val = axis_requested.values
                    ax_full = np.concatenate(
                        (
                            np.array([ax_val[0] - ax_val[1]]),
                            ax_val,
                            np.array([ax_val[-1] + ax_val[1] - ax_val[0]]),
                        )
                    )
                    # Swap axis to always have derivating axis on 1st position
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
            else:
                raise AxisError(
                    "Derivation not available except for time/angle/freqs axes"
                )

    if is_squeeze:
        values = np.squeeze(values)

    if unit == self.unit or unit == "SI":
        if is_norm:
            try:
                values = self.normalizations["ref"].normalize(values)
            except Exception:
                raise NormError("Reference value not specified for normalization")
    elif unit == "dB":
        ref_value = 1.0
        if "ref" in self.normalizations:
            ref_value *= self.normalizations["ref"].ref
        values = to_dB(np.abs(values), self.unit, ref_value)
    elif unit == "dBA":
        ref_value = 1.0
        if "ref" in self.normalizations:
            ref_value *= self.normalizations["ref"].ref
        for axis in axes_list:
            is_match = False
            if axis.name == "freqs" or axis.corr_name == "freqs":
                if axis.corr_values is not None and axis.unit not in [
                    "SI",
                    axis.corr_unit,
                ]:
                    axis_values = axis.corr_values
                else:
                    axis_values = axis.values
                index = axis.index
                values = np.apply_along_axis(
                    to_dBA, index, values, axis_values, self.unit, ref_value
                )
                is_match = True
            elif axis.name == "frequency":
                if axis.corr_values is None:
                    axis_values = axis.values
                else:
                    axis_values = axis.corr_values
                index = axis.index
                values = np.apply_along_axis(
                    to_dBA, index, values, axis_values, self.unit, ref_value
                )
                is_match = True
        if not is_match:
            raise UnitError("dBA conversion only available for fft with frequencies")
    elif unit in self.normalizations:
        values = self.normalizations.get(unit).normalize(values)
    else:
        values = convert_unit(values, self.unit, unit)

    return values
