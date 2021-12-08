from numpy import take
from SciDataTool.Functions.symmetries import rebuild_symmetries


def _get_field(self, axes_list):
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
        if axis_requested.is_pattern and (
            axis_requested.transform == "fft"
            or axis_requested.extension
            in [
                "sum",
                "rss",
                "mean",
                "rms",
                "integrate",
                "integrate_local",
                "derivate",
                "antiderivate",
            ]
            and axis_requested.is_pattern
        ):
            # DataPattern case where all values are requested
            values = take(values, axis_requested.rebuild_indices, axis_requested.index)
        elif axis_requested.transform == "fft" and "antiperiod" in axis_symmetries:
            # FFT case if axis is anti-periodic
            nper = axis_symmetries["antiperiod"]
            axis_symmetries["antiperiod"] = 2
            values = rebuild_symmetries(values, axis_requested.index, axis_symmetries)
            axis_symmetries["antiperiod"] = nper
        elif (
            axis_requested.indices is not None
            and max(axis_requested.indices) > values.shape[axis_requested.index]
        ):
            # Slicing case where requested indices are among other periods
            values = rebuild_symmetries(values, axis_requested.index, axis_symmetries)
            self.axes[axis_requested.index].symmetries = dict()

    return values
