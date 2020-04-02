# -*- coding: utf-8 -*-
from numpy import linspace
def get_values(self):
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
    return linspace(initial, final, number, endpoint=self.include_endpoint)
