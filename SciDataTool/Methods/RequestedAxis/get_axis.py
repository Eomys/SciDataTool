# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.interpolations import get_common_base
from numpy import array
from importlib import import_module


def get_axis(self, axis, normalizations):
    """Computes the vector 'axis' in the unit required, using conversions and symmetries if needed.
    Parameters
    ----------
    self: RequestedAxis
        a RequestedAxis object
    axis: Axis
        an Axis object
    normalizations: dict
        dictionary of the normalizations
    """
    is_components = getattr(axis, "is_components", False)
    if is_components:
        self.values = None
    else:
        # Get original values of the axis
        if self.operation is not None:
            module = import_module("SciDataTool.Functions.conversions")
            func = getattr(module, self.operation) # Conversion function
            values = array(func(axis.get_values()))
        else:
            values = array(axis.get_values())
        # Unit conversions and normalizations
        unit = self.unit
        if unit == self.corr_unit or unit == "SI":
            pass
        elif unit in normalizations:
            values = array([v / normalizations.get(unit) for v in values])
        else:
            values = convert(values, self.corr_unit, unit)
        # Interpolate axis with input data
        if self.extension == "whole":
            self.values = values
        elif self.input_data is not None:
            self.input_data = get_common_base(self.input_data, values)
            self.values = values
        elif self.indices is not None:
            self.values = values[self.indices]
                    
