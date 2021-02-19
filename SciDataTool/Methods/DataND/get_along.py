# -*- coding: utf-8 -*-
from SciDataTool.Functions.parser import read_input_strings
from SciDataTool.Functions.fft_functions import comp_fftn, comp_ifftn


def get_along(self, *args, unit="SI", is_norm=False, axis_data=[], is_squeeze=True):
    """Returns the ndarray of the field, using conversions and symmetries if needed.
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
    list of 1Darray of axes values, ndarray of field values
    """
    # Read the axes input in args
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args
    axes_list = read_input_strings(args, axis_data)
    # Extract the requested axes (symmetries + unit)
    axes_list, transforms = self.comp_axes(axes_list)
    # Get the field
    values = self.get_field(axes_list)
    # Inverse fft
    if "ifft" in transforms:
        values = comp_ifftn(values, axes_list, is_real=self.is_real)
    # Slices along time/space axes
    values, axes_dict_other = self.extract_slices(values, axes_list)
    # fft
    if "fft" in transforms:
        values = comp_fftn(values, axes_list, is_real=self.is_real)
    # Slices along fft axes
    values = self.extract_slices_fft(values, axes_list)
    # Rebuild symmetries
    values = self.rebuild_symmetries(values, axes_list)
    # Interpolate over axis values
    values = self.interpolate(values, axes_list, is_squeeze=is_squeeze)
    # Conversions
    values = self.convert(values, unit, is_norm, axes_list)
    # Return axes and values
    return_dict = {}
    for axis_requested in axes_list:
        if axis_requested.extension in ["sum", "rss", "mean", "rms"]:
            return_dict[axis_requested.name] = axis_requested.extension
        else:
            return_dict[axis_requested.name] = axis_requested.values
    return_dict[self.symbol] = values
    return_dict["axes_list"] = axes_list
    return_dict["axes_dict_other"] = axes_dict_other
    return return_dict
