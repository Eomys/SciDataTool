# -*- coding: utf-8 -*-
from SciDataTool.Functions.fft_functions import comp_fft, comp_ifft
from SciDataTool.Functions.conversions import rphiz_to_xyz_field, xyz_to_rphiz_field
from numpy import apply_along_axis

def transform(self, values, axes_list):
    """Returns the values of the field transformed or converted.
    Parameters
    ----------
    self: Data
        a Data object
    values: ndarray
        array of the field
    axes_list: list
        a list of RequestedAxis objects
    Returns
    -------
    values: ndarray
        values of the transformed field
    """
    
    is_fft = True
    for axis_requested in axes_list:
        # Transform (fft, coordinates, etc)
        if axis_requested.transform == "fft" and is_fft:
            values = comp_fft(values)
            is_fft = False
        elif axis_requested.transform == "ifft" and is_fft:
            values = comp_ifft(values)
            is_fft = False
        if axis_requested.transform == "pol2cart":
            values = apply_along_axis(rphiz_to_xyz_field, axis_requested.index, values, axis_requested.values[:,1])
        elif axis_requested.transform == "cart2pol":
            values = apply_along_axis(xyz_to_rphiz_field, axis_requested.index, values, axis_requested.values[:,1])
    return values