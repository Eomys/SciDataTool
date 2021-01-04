# -*- coding: utf-8 -*-
from SciDataTool import Data1D
from SciDataTool.Functions import AxisError, axes_dict, rev_axes_dict


def get_data_along(self, *args, unit="SI", is_norm=False, axis_data=[]):
    """Returns the sliced or interpolated version of the data, using conversions and symmetries if needed.
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
    a DataND object
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataND", fromlist=["DataND"])
    DataND = getattr(module, "DataND")

    results = self.get_along(*args)
    values = results.pop(self.symbol)
    del results["axes_dict_other"]
    del results["axes_list"]
    Axes = []
    for axis_name in results.keys():
        if len(results[axis_name]) > 1:
            for axis in self.axes:
                if axis.name == axis_name:
                    name = axis.name
                    is_components = axis.is_components
                    axis_values = results[axis_name]
                    unit = axis.unit
                elif axis_name in axes_dict:
                    if axes_dict[axis_name][0] == axis.name:
                        name = axis_name
                        is_components = axis.is_components
                        axis_values = results[axis_name]
                        unit = axes_dict[axis_name][2]
                elif axis_name in rev_axes_dict:
                    if rev_axes_dict[axis_name][0] == axis.name:
                        name = axis_name
                        is_components = axis.is_components
                        axis_values = results[axis_name]
                        unit = rev_axes_dict[axis_name][2]
            Axes.append(
                Data1D(
                    name=name,
                    unit=unit,
                    values=axis_values,
                    is_components=is_components,
                )
            )
    return DataND(
        name=self.name,
        unit=self.unit,
        symbol=self.symbol,
        axes=Axes,
        values=values,
        is_real=self.is_real,
    )
