# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.interpolations import get_common_base
from SciDataTool.Classes.DataPattern import DataPattern
from SciDataTool.Functions import AxisError
from numpy import array
from importlib import import_module


def get_axis(self, axis):
    """Computes the vector 'axis' in the unit required, using conversions and symmetries if needed.
    Parameters
    ----------
    self: RequestedAxis
        a RequestedAxis object
    axis: Axis
        an Axis object
    """
    if isinstance(axis, DataPattern):
        self.is_pattern = True
        self.rebuild_indices = axis.rebuild_indices
        self.is_step = axis.is_step
    is_components = getattr(axis, "is_components", False)
    if is_components:
        values = axis.get_values()
        if self.extension != "sum" or self.extension != "rms":
            self.extension = "list"
        if self.indices is not None:
            self.values = values[self.indices]
        else:
            self.values = values
    else:
        if self.extension == "pattern":
            if not self.is_pattern:
                raise AxisError(
                    "ERROR: [pattern] cannot be called with non DataPattern axis"
                )
            else:
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
                self.extension = "smallestperiod"
        elif self.extension == "smallestperiod":
            if isinstance(axis, DataPattern):
                raise AxisError(
                    "ERROR: [smallestperiod] cannot be called with DataPattern axis"
                )
            else:
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
        elif self.extension == "antiperiod":
            if isinstance(axis, DataPattern):
                raise AxisError(
                    "ERROR: [antiperiod] cannot be called with DataPattern axis"
                )
            else:
                is_smallestperiod = False
                is_oneperiod = False
                is_antiperiod = True
        elif self.extension == "oneperiod" or self.transform == "fft":
            if isinstance(axis, DataPattern):
                raise AxisError(
                    "ERROR: [oneperiod] cannot be called with DataPattern axis"
                )
            else:
                is_smallestperiod = False
                is_oneperiod = True
                is_antiperiod = False
        elif self.extension == "axis_data":
            is_smallestperiod = False
            is_oneperiod = False
            is_antiperiod = False
        else:
            is_smallestperiod = False
            is_oneperiod = False
            is_antiperiod = False
        # Get original values of the axis
        if self.operation is not None:
            module = import_module("SciDataTool.Functions.conversions")
            func = getattr(module, self.operation)  # Conversion function
            values = array(
                func(
                    axis.get_values(
                        is_oneperiod=is_oneperiod,
                        is_antiperiod=is_antiperiod,
                        is_smallestperiod=is_smallestperiod,
                    )
                )
            )
        else:
            values = array(
                axis.get_values(
                    is_oneperiod=is_oneperiod,
                    is_antiperiod=is_antiperiod,
                    is_smallestperiod=is_smallestperiod,
                )
            )
        # Unit conversions and normalizations
        unit = self.unit
        if unit == self.corr_unit or unit == "SI":
            pass
        elif unit in axis.normalizations:
            if axis.normalizations.get(unit) == "indices":
                values = array([i for i in range(len(values))])
            else:
                values = array([v / axis.normalizations.get(unit) for v in values])
        else:
            values = convert(values, self.corr_unit, unit)
        # Rebuild symmetries in fft case
        if self.transform == "fft":
            if "period" in axis.symmetries:
                if axis.name != "time":
                    values = values * axis.symmetries["period"]
            elif "antiperiod" in axis.symmetries:
                if axis.name != "time":
                    values = values * axis.symmetries["antiperiod"] / 2
        # Interpolate axis with input data
        if self.extension in ["whole", "oneperiod", "antiperiod", "smallestperiod"]:
            self.values = values
        elif self.input_data is not None:
            if len(self.input_data) == 2 and self.extension != "axis_data":
                self.indices = [
                    i
                    for i, x in enumerate(values)
                    if x >= self.input_data[0] and x <= self.input_data[-1]
                ]
                self.input_data = None
            else:
                if self.extension == "axis_data":
                    if self.is_step:
                        self.input_data = self.input_data
                    else:
                        self.input_data = get_common_base(
                            self.input_data, values, is_downsample=True
                        )
                else:
                    self.input_data = get_common_base(self.input_data, values)
                self.values = values
        if self.indices is not None:
            self.values = values[self.indices]
