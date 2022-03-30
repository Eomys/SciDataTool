from SciDataTool.Functions.symmetries import (
    rebuild_symmetries as rebuild_symmetries_fct,
)

from numpy import take


def _rebuild_symmetries(
    self,
    values,
    axes_list,
):
    """Reconstructs the field of a Data object taking symmetries into account
    Parameters
    ----------
    self: Data
        a Data object
    values: ndarray
        ndarray of a field
    axes_list: list
        a list of RequestedAxis objects
    Returns
    -------
    ndarray of the reconstructed field
    """

    for axis in axes_list:
        if (
            axis.transform != "fft"
            and axis.is_pattern
            and (
                axis.extension
                not in [
                    "max",
                    "min",
                    "sum",
                    "rss",
                    "mean",
                    "rms",
                    "integrate",
                    "integrate_local",
                    "derivate",
                    "smallestperiod",
                ]
                and axis.indices is None
            )
        ):
            values = take(values, axis.rebuild_indices, axis.index)
        elif axis.transform != "fft" and axis.extension in [
            "whole",
            "interval",
            "oneperiod",
            "antiperiod",
            "smallestperiod",
        ]:
            if axis.extension == "smallestperiod":
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
            elif axis.extension == "antiperiod":
                is_smallestperiod = False
                is_oneperiod = False
                is_antiperiod = True
            elif axis.extension == "oneperiod":
                is_smallestperiod = False
                is_oneperiod = True
                is_antiperiod = False
            # Ignore symmetries if fft axis
            elif axis.name in ["freqs", "wavenumber"]:
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
            # Ignore symmetries if non uniform ifft was used
            elif (
                axis.transform == "ifft"
                # and len(axis.values) != len(axis.corr_values)
                and len(axis.values) == values.shape[axis.index]
            ):
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
            else:
                is_smallestperiod = False
                is_oneperiod = False
                is_antiperiod = False

            # Rebuild symmetries
            axis_symmetries = self.axes[axis.index].symmetries
            if is_oneperiod:
                if "antiperiod" in axis_symmetries:
                    nper = axis_symmetries["antiperiod"]
                    axis_symmetries["antiperiod"] = 2
                    values = rebuild_symmetries_fct(values, axis.index, axis_symmetries)
                    axis_symmetries["antiperiod"] = nper
            elif not is_smallestperiod and not is_antiperiod:
                values = rebuild_symmetries_fct(values, axis.index, axis_symmetries)
    return values
