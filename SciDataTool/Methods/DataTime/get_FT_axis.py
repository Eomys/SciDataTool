# -*- coding: utf-8 -*-
from SciDataTool.Functions import AxisError
from SciDataTool.Functions.fft_functions import comp_fft_freqs
from SciDataTool.Functions.conversions import convert
from numpy import array, argmin, abs as np_abs, argwhere, ravel


def get_FT_axis(self, axis_str, is_positive=False):
    """Returns the vector 'axis' for the Fourier Transform in the unit required, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    axis_str: str
        The name of the axis, its range and unit (optional)
    is_positive: bool
        Boolean indicating whether only the positive frequencies must be computed
    Returns
    -------
    Array of axis values
    """
    # Read the input string
    unit = "SI"
    # Detect unit
    if "{" in axis_str:
        elems = axis_str.split("{")
        unit = elems[1].strip("}")
        axis_name = elems[0]
    else:
        axis_name = axis_str
    if axis_name == "freqs":
        for axis in self.axes:
            if axis.name == "time":
                # Get fft axis
                is_time = True
                values = array(comp_fft_freqs(axis.get_values(), is_time, is_positive))
                # Conversion to unit
                if unit == "Hz" or unit == "SI":
                    pass
                elif unit in self.normalizations:
                    values = array([v / self.normalizations.get(unit) for v in values])
                else:
                    values = convert(values, axis.unit, unit)
                return values
        raise AxisError("ERROR: Requested axis [" + axis_name + "] is not available")
    if axis_name == "wavenumber":
        for axis in self.axes:
            if axis.name == "angle":
                # Get fft axis
                is_time = False
                values = array(comp_fft_freqs(axis.get_values(), is_time, is_positive))
                # Conversion to unit
                if unit == "SI":
                    pass
                elif unit in self.normalizations:
                    values = array([v / self.normalizations.get(unit) for v in values])
                else:
                    values = convert(values, axis.unit, unit)
                return values
        raise AxisError("ERROR: Requested axis [" + axis_name + "] is not available")
    else:  # Slice
        for axis in self.axes:
            if axis.name == axis_name:
                values = array(axis.get_values())
                # Conversion to unit
                if unit == "SI":
                    pass
                elif unit in self.normalizations:
                    values = array([v / self.normalizations.get(unit) for v in values])
                else:
                    values = convert(values, axis.unit, unit)
                return values
        raise AxisError("ERROR: Requested axis [" + axis_name + "] is not available")
