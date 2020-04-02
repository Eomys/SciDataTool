# -*- coding: utf-8 -*-
from SciDataTool.Functions.interpolations import get_common_base, get_interpolation
from numpy import squeeze
def compare_phase_along(self, *args, unit="SI", data_list=[], is_norm=False):
    """Returns the ndarrays of both fields interpolated in the same axes, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    data_list: list
        list of Data objects to compare
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    Returns
    -------
    list of 1Darray of axis values, ndarrays of fields
    """
    if data_list == []:
        (axis, values) = self.get_phase_along(args, unit=unit, is_norm=is_norm)
        return (axis, [values])
    else:
        # Extract requested axes + field values
        result_list = self.get_phase_along(args, unit=unit, is_norm=is_norm)
        values = result_list[-1]
        axes = result_list[:-1]
        data_axis_values = []
        data_values = []
        for data in data_list:
            result_list = data.get_phase_along(args, unit=unit, is_norm=is_norm)
            data_values.append(result_list[-1])
            data_axis_values.append(result_list[:-1])
        # Get the common bases
        common_axis_values = []
        for index, axis in enumerate(axes):
            common_axis_values.append(axis)
            for i, data in enumerate(data_list):
                common_axis_values[index] = get_common_base(
                    common_axis_values[index], data_axis_values[i][index]
                )
            # Interpolate over common axis values
            values = get_interpolation(values, axis, common_axis_values[index])
            for i, data in enumerate(data_list):
                data_values[i] = get_interpolation(
                    data_values[i],
                    data_axis_values[i][index],
                    common_axis_values[index],
                )
        # Return axis and values
        return (squeeze(common_axis_values), [values] + data_values)
