# -*- coding: utf-8 -*-
from SciDataTool.Functions import NormError, UnitError
from SciDataTool.Functions.conversions import convert, to_dB, to_dBA, to_noct
from numpy import apply_along_axis, abs as np_abs


def get_magnitude_along(
    self, *args, unit="SI", is_norm=False, axis_data=[], is_squeeze=True
):
    """Returns the ndarray of the magnitude of the FT, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    axis_data: list
        list of ndarray corresponding to user-input data
    Returns
    -------
    list of 1Darray of axes values, ndarray of magnitude values
    """
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args
    return_dict = self.get_along(
        args, axis_data=axis_data, is_squeeze=is_squeeze, is_magnitude=True
    )
    values = return_dict[self.symbol]

    # 1/nth octave band
    for axis in return_dict["axes_list"]:
        if axis.name == "freqs" or axis.corr_name == "freqs":
            index = axis.index
            if axis.noct is not None:
                (values, foct) = apply_along_axis(
                    to_noct, index, values, return_dict["freqs"], noct=axis.noct
                )
                return_dict[axis.name] = foct
    # Convert into right unit (apart because of dBA conversion)
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
        values = to_dB(values, self.unit, ref_value)
    elif unit == "dBA":
        ref_value = 1.0
        if "ref" in self.normalizations.keys():
            ref_value *= self.normalizations.get("ref")
        if "freqs" in return_dict.keys():
            for axis in return_dict["axes_list"]:
                if axis.name == "freqs" or axis.corr_name == "freqs":
                    index = axis.index
            values = apply_along_axis(
                to_dBA, index, values, return_dict["freqs"], self.unit, ref_value
            )
        else:
            raise UnitError(
                "ERROR: dBA conversion only available for fft with frequencies"
            )
    elif unit in self.normalizations:
        values = values / self.normalizations.get(unit)
    else:
        values = convert(values, self.unit, unit)
    return_dict[self.symbol] = values
    return return_dict
