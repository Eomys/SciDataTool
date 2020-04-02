# -*- coding: utf-8 -*-
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
def get_values(self):
    """Returns the vector 'axis' taking symmetries into account (no units).
    Parameters
    ----------
    self: Data1D
        a Data1D object
    Returns
    -------
    Vector of axis values
    """
    values = self.values
    # Rebuild symmetries
    if self.name in self.symmetries:
        values = rebuild_symmetries_axis(values, self.symmetries.get(self.name))
    return values
