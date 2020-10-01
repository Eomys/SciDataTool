# -*- coding: utf-8 -*-
from SciDataTool.Functions.symmetries import rebuild_symmetries as rebuild_symmetries_fct

def rebuild_symmetries(self, values, axes_list):
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
    for axis_requested in axes_list:
        # Rebuild symmetries
        if(
            axis_requested.transform == "fft"
            and axis_requested.corr_name in self.symmetries.keys()
        ):
            if "antiperiod" in self.symmetries.get(axis_requested.corr_name):
                nper = self.symmetries.get(axis_requested.corr_name)["antiperiod"]
                self.symmetries.get(axis_requested.corr_name)["antiperiod"] = 2
                values = rebuild_symmetries_fct(
                    values, axis_requested.index, self.symmetries.get(axis_requested.corr_name)
                )
        if(
            axis_requested.transform != "fft"
            and axis_requested.indices is None
            and axis_requested.corr_name in self.symmetries.keys()
        ):
            values = rebuild_symmetries_fct(
                values, axis_requested.index, self.symmetries.get(axis_requested.corr_name)
            )
    return values    
