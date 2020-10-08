# -*- coding: utf-8 -*-
from SciDataTool.Functions.symmetries import (
    rebuild_symmetries as rebuild_symmetries_fct,
)
from SciDataTool.Functions import AxisError


def rebuild_symmetries(
    self, values, axis_name, axis_index, is_oneperiod=False, is_antiperiod=False
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
    # Rebuild symmetries
    if is_antiperiod:
        if axis_name in self.symmetries.keys():
            if "antiperiod" in self.symmetries.get(axis_name):
                return values
            else:
                raise AxisError("ERROR: axis has no antiperiodicity")
        else:
            raise AxisError("ERROR: axis has no antiperiodicity")
    elif is_oneperiod:
        if axis_name in self.symmetries:
            if "antiperiod" in self.symmetries.get(axis_name):
                nper = self.symmetries.get(axis_name)["antiperiod"]
                self.symmetries.get(axis_name)["antiperiod"] = 2
                values = rebuild_symmetries_fct(
                    values, axis_index, self.symmetries.get(axis_name)
                )
                self.symmetries.get(axis_name)["antiperiod"] = nper
                return values
            else:
                return values
        else:
            return values
    else:
        if axis_name in self.symmetries:
            values = rebuild_symmetries_fct(
                values, axis_index, self.symmetries.get(axis_name)
            )
            return values
        else:
            return values
