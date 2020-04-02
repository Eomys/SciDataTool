# -*- coding: utf-8 -*-

from pyleecan.Functions.FT import AxisError
from pyleecan.Functions.FT.fft_functions import comp_fft_time
from pyleecan.Functions.FT.conversions import convert
from numpy import array


def get_axis(self, axis_str):
    """Returns the vector 'axis' for the Inverse Fourier Transform in the unit required, using conversions and symmetries if needed.

    Parameters
    ----------
    self: Data
        a Data object
    axis_str: str
        The name of the axis, its range and unit (optional)
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

    if axis_name == "time":
        for axis in self.axes:
            if axis.name == "freqs":
                # Get fft axis
                values = array(comp_fft_time(axis.get_values(), is_angle=False))

                # Conversion to unit
                if unit == "s" or unit == "SI":
                    pass
                elif unit in self.normalizations:
                    values = array([v / self.normalizations.get(unit) for v in values])
                else:
                    values = convert(values, "s", unit)

                return values

        raise AxisError("ERROR: Requested axis [" + axis_name + "] is not available")

    if axis_name == "angle":
        for axis in self.axes:
            if axis.name == "wavenumber":
                # Get fft axis
                values = array(comp_fft_time(axis.get_values(), is_angle=True))

                # Conversion to unit
                if unit == "rad" or unit == "SI":
                    pass
                elif unit in self.normalizations:
                    values = array([v / self.normalizations.get(unit) for v in values])
                else:
                    values = convert(values, "rad", unit)

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


# Todo: add wavenumberx...
