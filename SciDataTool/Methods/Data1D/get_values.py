# -*- coding: utf-8 -*-
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis


def get_values(self, is_fft=False):
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
    if self.name in self.symmetries and is_fft:
        if "antiperiod" in self.symmetries:
            nper = self.symmetries["antiperiod"]
            self.symmetries["antiperiod"] = 2
            values = rebuild_symmetries_axis(values, self.symmetries)
            del self.symmetries["antiperiod"]
            self.symmetries["period"] = nper
    return values
