# -*- coding: utf-8 -*-
from numpy import sum as np_sum, mean as np_mean, sqrt
from SciDataTool.Functions.symmetries import rebuild_symmetries


def get_field(self, axes_list):
    """Returns the values of the field (with symmetries and sums).
    Parameters
    ----------
    self: Data
        a Data object
    axes_list: list
        a list of RequestedAxis objects
    Returns
    -------
    values: ndarray
        values of the field
    """

    values = self.values
    for axis_requested in axes_list:
        # Rebuild symmetries for fft case
        axis_symmetries = self.axes[axis_requested.index].symmetries
        if axis_requested.transform == "fft" and axis_requested.is_pattern:
            values = values[axis_requested.rebuild_indices]
        elif axis_requested.transform == "fft" and "antiperiod" in axis_symmetries:
            nper = axis_symmetries["antiperiod"]
            axis_symmetries["antiperiod"] = 2
            values = rebuild_symmetries(
                values, axis_requested.index, axis_symmetries)
            axis_symmetries["antiperiod"] = nper

        # sum over sum axes
        if axis_requested.extension == "sum":
            values = np_sum(values, axis=axis_requested.index, keepdims=True)
        # mean value over mean axes
        elif axis_requested.extension == "mean":
            values = np_mean(values, axis=axis_requested.index, keepdims=True)
        # RMS over rms axes
        elif axis_requested.extension == "rms":
            values = sqrt(
                np_sum(values ** 2, axis=axis_requested.index, keepdims=True))
    return values
