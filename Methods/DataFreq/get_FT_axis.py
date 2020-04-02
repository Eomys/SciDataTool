# -*- coding: utf-8 -*-
from SciDataTool.Functions.FT import AxisError
from SciDataTool.Functions.FT.conversions import convert
from numpy import array
def get_FT_axis(self, axis_str):
    """Returns the vector 'axis' in the unit required, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    axis_str: str
        The name of the axis, its range and unit (optional)
    Returns
    -------
    Vector of axis values
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
    # Check if axis exists in the axes list
    for axis in self.axes:
        if axis.name == axis_name:
            values = array(axis.get_values())  # Rebuilt with symmetries
            # Conversions and normalizations
            if unit == axis.unit or unit == "SI":
                pass
            elif unit in self.normalizations:
                values = array([v / self.normalizations.get(unit) for v in values])
            else:
                values = convert(values, axis.unit, unit)
            return values
    raise AxisError("ERROR: Requested axis [" + axis_name + "] is not available")
