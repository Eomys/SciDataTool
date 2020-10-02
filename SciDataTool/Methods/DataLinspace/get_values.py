# -*- coding: utf-8 -*-
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from numpy import linspace


def get_values(self, is_fft=False):
    """Returns the vector 'axis' by rebuilding the linspace.
    Parameters
    ----------
    self: Data1D
        a Data1D object
    Returns
    -------
    Vector of axis values
    """
    initial = self.initial
    if self.number == None:
        final = self.final
        number = (final - initial + self.step) / self.step
    elif self.final == None:
        number = self.number
        final = self.initial + (number - 1) * self.step
    else:
        number = self.number
        final = self.final
    values = linspace(initial, final, int(number), endpoint=self.include_endpoint)
    # Rebuild symmetries
    if self.name in self.symmetries and is_fft:
        if "antiperiod" in self.symmetries:
            nper = self.symmetries["antiperiod"]
            self.symmetries["antiperiod"] = 2
            values = rebuild_symmetries_axis(values, self.symmetries.get(self.name))
            del self.symmetries["antiperiod"]
            self.symmetries["period"] = nper
    return values
