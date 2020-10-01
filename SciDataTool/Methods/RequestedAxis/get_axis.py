# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.interpolations import get_common_base
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
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
        if self.transform == "fft":
            is_fft = True
        else:
            is_fft = False
        # Get original values of the axis
        if self.operation is not None:
            module = import_module("SciDataTool.Functions.conversions")
            func = getattr(module, self.operation) # Conversion function
            values = array(func(axis.get_values(is_fft)))
        else:
            values = array(axis.get_values(is_fft))
        # Unit conversions and normalizations
        unit = self.unit
        if unit == self.corr_unit or unit == "SI":
            pass
        elif unit in normalizations:
            values = array([v / normalizations.get(unit) for v in values])
        else:
            values = convert(values, self.corr_unit, unit)
        # Rebuild symmetries
        if is_fft and axis.name in axis.symmetries:
            if "period" in axis.symmetries.get(axis.name).keys():
                values = values * axis.symmetries.get(axis.name).get("period")
            elif "antiperiod" in axis.symmetries.keys():
                values = values * axis.symmetries.get(axis.name).get("antiperiod")
        elif axis.name in axis.symmetries:
            values = rebuild_symmetries_axis(values, axis.symmetries.get(axis.name))
        # Interpolate axis with input data
        if self.extension == "whole":
            self.values = values
        elif self.input_data is not None:
            self.input_data = get_common_base(self.input_data, values)
            self.values = values
        elif self.indices is not None:
            self.values = values[self.indices]
                    
