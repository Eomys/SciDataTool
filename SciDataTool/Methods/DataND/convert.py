import numpy as np

from SciDataTool.Functions import NormError, UnitError, AxisError
from SciDataTool.Functions.conversions import convert as convert_unit, to_dB, to_dBA
from SciDataTool.Functions.derivation_integration import (
    derivate,
    integrate,
    antiderivate,
)


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
        # Get axis data
        extension = axis_requested.extension
        index = axis_requested.index
        # sum over sum axes
        if extension in "sum":
            values = np.sum(values, axis=index, keepdims=True)
        # root sum square over rss axes
        elif extension == "rss":
            if axis_requested.name in ["time", "angle", "z"]:
                # Use trapz rather than sum
                values = np.sqrt(
                    integrate(values ** 2, axis_requested.values, index, is_aper)
                )
            else:
                values = np.sqrt(np.sum(values ** 2, axis=index, keepdims=True))
        # mean value over mean axes
        elif extension == "mean":
            if axis_requested.name in ["time", "angle", "z"]:
                # Use trapz/interval rather than mean
                ax_val = axis_requested.values
                values = integrate(
                    values ** 2, axis_requested.values, index, is_aper, is_mean=True
                )
            else:
                values = np.mean(values, axis=index, keepdims=True)

        # RMS over rms axes
        elif extension == "rms":
            values = np.sqrt(np.mean(values ** 2, axis=index, keepdims=True))
        # integration over integration axes
        elif extension == "integrate":
            if axis_requested.name in ["time", "angle", "z"]:
                ax_val = axis_requested.values
                _, is_aper = self.axes[index].get_periodicity()
                values = integrate(values, ax_val, index, is_aper)
            else:
                raise AxisError("Integration not available except for time/angle/z")
        # integration over integration axes
        elif extension == "antiderivate":
            if axis_requested.name == "freqs":
                dim_array = np.ones((1, values.ndim), int).ravel()
                dim_array[index] = -1
                axis_reshaped = axis_requested.values.reshape(dim_array)
                axis_reshaped[axis_reshaped == 0] = np.inf  # put f=0 component to 0
                values = values / (axis_reshaped * 2 * 1j * np.pi)
            elif axis_requested.name in ["time", "angle", "z"]:
                ax_val = axis_requested.values
                _, is_aper = self.axes[index].get_periodicity()
                values = antiderivate(values, ax_val, index, is_aper)
            else:
                raise AxisError(
                    "Anti derivation not available except for time/angle/z/freqs axes"
                )
        # derivation over derivation axes
        elif extension == "derivate":
            if axis_requested.name == "freqs":
                dim_array = np.ones((1, values.ndim), int).ravel()
                dim_array[index] = -1
                axis_reshaped = axis_requested.values.reshape(dim_array)
                values = values * axis_reshaped * 2 * 1j * np.pi
            elif axis_requested.name in ["time", "angle"]:
                ax_val = axis_requested.values
                _, is_aper = self.axes[index].get_periodicity()
                values = derivate(values, ax_val, index, is_aper)
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
