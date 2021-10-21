import numpy as np

from SciDataTool.Functions import NormError, UnitError, AxisError
from SciDataTool.Functions.conversions import convert as convert_unit, to_dB, to_dBA
from SciDataTool.Functions.derivation_integration import (
    derivate,
    integrate,
    antiderivate,
)
from SciDataTool.Functions.sum_mean import (
    my_sum,
    my_mean,
    root_mean_square,
    root_sum_square,
)


def convert(self, values, unit, is_norm, is_squeeze, axes_list):
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
