# -*- coding: utf-8 -*-
from SciDataTool.Functions.fft_functions import comp_fft, comp_ifft
from SciDataTool.Functions.conversions import rphiz_to_xyz_field, xyz_to_rphiz_field
from numpy import apply_along_axis, apply_over_axes

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
    
    #is_fft = True
    #values = comp_fft(values, axes=[axis_requested.index for axis_requested in axes_list if axis_requested.transform == "fft"])
    for axis_requested in axes_list:
        
        # Transform (fft, coordinates, etc)
        if axis_requested.transform == "fft":
            values = apply_along_axis(comp_fft, axis_requested.index, values)
        elif axis_requested.transform == "ifft":
            values = apply_along_axis(comp_ifft, axis_requested.index, values)
        if axis_requested.transform == "pol2cart":
            values = apply_along_axis(rphiz_to_xyz_field, axis_requested.index, values, axis_requested.values[:,1])
        elif axis_requested.transform == "cart2pol":
            values = apply_along_axis(xyz_to_rphiz_field, axis_requested.index, values, axis_requested.values[:,1])
    return values