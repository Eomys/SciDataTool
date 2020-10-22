# -*- coding: utf-8 -*-
from numpy import sum as np_sum
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
        # Rebuild symmetries only for fft case
        axis_symmetries = self.axes[axis_requested.index].symmetries
        if (
            axis_requested.transform == "fft"
            and "antiperiod" in axis_symmetries
        ):
            nper = axis_symmetries["antiperiod"]
            axis_symmetries["antiperiod"] = 2
            values = rebuild_symmetries(
                values, axis_requested.index, axis_symmetries
            )
            axis_symmetries["antiperiod"] = nper

        # Sum over sum axes
        if axis_requested.extension == "sum":
            values = np_sum(values, axis=axis_requested.index)
    return values
