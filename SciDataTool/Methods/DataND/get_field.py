# -*- coding: utf-8 -*-
from numpy import (
    sum as np_sum,
    mean as np_mean,
    sqrt,
    trapz,
    take,
    min as np_min,
    max as np_max,
)
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
        # Rebuild symmetries when needed
        axis_symmetries = self.axes[axis_requested.index].symmetries
        if (
            axis_requested.transform == "fft"
            and axis_requested.is_pattern
            or axis_requested.extension in ["sum", "rss", "mean", "rms", "integrate"]
            and axis_requested.is_pattern
        ):
            values = take(values, axis_requested.rebuild_indices, axis_requested.index)
        elif axis_requested.transform == "fft" and "antiperiod" in axis_symmetries:
            nper = axis_symmetries["antiperiod"]
            axis_symmetries["antiperiod"] = 2
            values = rebuild_symmetries(values, axis_requested.index, axis_symmetries)
            axis_symmetries["antiperiod"] = nper
        elif axis_requested.indices is not None:
            if (
                axis_requested.extension in ["sum", "rss", "mean", "rms", "integrate"]
                or max(axis_requested.indices) > values.shape[axis_requested.index]
            ):
                values = rebuild_symmetries(
                    values, axis_requested.index, axis_symmetries
                )
                self.axes[axis_requested.index].symmetries = dict()

        # # sum over sum axes
        # if axis_requested.extension == "sum":
        #     values = np_sum(values, axis=axis_requested.index, keepdims=True)
        # # root sum square over rss axes
        # elif axis_requested.extension == "rss":
        #     values = sqrt(np_sum(values ** 2, axis=axis_requested.index, keepdims=True))
        # # mean value over mean axes
        # elif axis_requested.extension == "mean":
        #     values = np_mean(values, axis=axis_requested.index, keepdims=True)
        # # RMS over rms axes
        # elif axis_requested.extension == "rms":
        #     values = sqrt(
        #         np_mean(values ** 2, axis=axis_requested.index, keepdims=True)
        #     )
        # # integration over integration axes
        # elif axis_requested.extension == "integrate":
        #     values = trapz(
        #         values, x=axis_requested.values, axis=axis_requested.index
        #     ) / (np_max(axis_requested.values) - np_min(axis_requested.values))
    return values
