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
    # values = self.values
    # # Adapt fft axis
    # if is_fft and self.name in self.symmetries:
    #     if "period" in self.symmetries.keys():
    #         values = values * self.symmetries.get("period")
    #     elif "antiperiod" in self.symmetries.keys():
    #         values = values * self.symmetries.get("antiperiod")
    # # Rebuild symmetries
    # elif self.name in self.symmetries:
    #     values = rebuild_symmetries_axis(values, self.symmetries.get(self.name))
    return self.values
