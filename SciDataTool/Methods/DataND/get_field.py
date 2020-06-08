# -*- coding: utf-8 -*-
from SciDataTool.Functions.symmetries import rebuild_symmetries

def get_field(self, axes_list):
    """Returns the values of the field (with symmetries and transformations).
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
        # Rebuild symmetries
        if axis_requested.corr_name in self.symmetries.keys():
            values = rebuild_symmetries(
                values, axis_requested.index, self.symmetries.get(axis_requested.corr_name)
            )
    return values