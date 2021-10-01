# -*- coding: utf-8 -*-
from numpy import (
    abs as np_abs,
    sum as np_sum,
    mean as np_mean,
    sqrt,
    trapz,
    squeeze,
    min as np_min,
    max as np_max,
    apply_along_axis,
    pi,
    ones,
)

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
        values = np_abs(values)

    # Apply sums, means, etc
    for axis_requested in axes_list:
        # sum over sum axes
        if axis_requested.extension == "sum":
            values = np_sum(values, axis=axis_requested.index, keepdims=True)
        # root sum square over rss axes
        elif axis_requested.extension == "rss":
            values = sqrt(np_sum(values ** 2, axis=axis_requested.index, keepdims=True))
        # mean value over mean axes
        elif axis_requested.extension == "mean":
            values = np_mean(values, axis=axis_requested.index, keepdims=True)
        # RMS over rms axes
        elif axis_requested.extension == "rms":
            values = sqrt(
                np_mean(values ** 2, axis=axis_requested.index, keepdims=True)
            )
        # integration over integration axes
        elif axis_requested.extension == "integrate":
            if axis_requested.name == "freqs":
                dim_array = ones((1, values.ndim), int).ravel()
                dim_array[axis_requested.index] = -1
                axis_reshaped = axis_requested.values.reshape(dim_array)
                values = values / (axis_reshaped * 2 * 1j * pi)
            else:
                values = trapz(
                    values, x=axis_requested.values, axis=axis_requested.index
                ) / (np_max(axis_requested.values) - np_min(axis_requested.values))
        # derivation over derivation axes
        elif axis_requested.extension == "derivate":
            if axis_requested.name == "freqs":
                dim_array = ones((1, values.ndim), int).ravel()
                dim_array[axis_requested.index] = -1
                axis_reshaped = axis_requested.values.reshape(dim_array)
                values = values * axis_reshaped * 2 * 1j * pi
            else:
                raise AxisError("Derivation not available in time domain")

    if is_squeeze:
        values = squeeze(values)

    if unit == self.unit or unit == "SI":
        if is_norm:
            try:
                values = values / self.normalizations.get("ref")
            except:
                raise NormError(
                    "ERROR: Reference value not specified for normalization"
                )
    elif unit == "dB":
        ref_value = 1.0
        if "ref" in self.normalizations.keys():
            ref_value *= self.normalizations.get("ref")
        values = to_dB(np_abs(values), self.unit, ref_value)
    elif unit == "dBA":
        ref_value = 1.0
        if "ref" in self.normalizations.keys():
            ref_value *= self.normalizations.get("ref")
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
                values = apply_along_axis(
                    to_dBA, index, values, axis_values, self.unit, ref_value
                )
                is_match = True
            elif axis.name == "frequency":
                if axis.corr_values is None:
                    axis_values = axis.values
                else:
                    axis_values = axis.corr_values
                index = axis.index
                values = apply_along_axis(
                    to_dBA, index, values, axis_values, self.unit, ref_value
                )
                is_match = True
        if not is_match:
            raise UnitError(
                "ERROR: dBA conversion only available for fft with frequencies"
            )
    elif unit in self.normalizations:
        values = values / self.normalizations.get(unit)
    else:
        values = convert_unit(values, self.unit, unit)

    return values
