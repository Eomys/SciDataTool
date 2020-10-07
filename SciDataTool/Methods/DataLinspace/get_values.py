# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from SciDataTool.Functions import AxisError
from numpy import linspace


def get_values(self, unit="SI", is_oneperiod=False, is_antiperiod=False):
    """Returns the vector 'axis' by rebuilding the linspace, symmetries and unit included.
    Parameters
    ----------
    self: DataLinspace
        a DataLinspace object
    unit: str
        requested unit
    is_oneperiod: bool
        return values on a single period
    is_antiperiod: bool
        return values on a semi period (only for antiperiodic signals)
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

    # Unit conversion
    if unit != "SI" and unit != self.unit:
        values = convert(values, self.unit, unit)

    # Rebuild symmetries
    if is_antiperiod:
        if self.name in self.symmetries:
            if "antiperiod" in self.symmetries.get(self.name):
                return values
            else:
                raise AxisError("ERROR: axis has no antiperiodicity")
        else:
            raise AxisError("ERROR: axis has no antiperiodicity")
    elif is_oneperiod:
        if self.name in self.symmetries:
            if "antiperiod" in self.symmetries.get(self.name):
                nper = self.symmetries.get(self.name)["antiperiod"]
                self.symmetries.get(self.name)["antiperiod"] = 2
                values = rebuild_symmetries_axis(values, self.symmetries.get(self.name))
                del self.symmetries.get(self.name)["antiperiod"]
                self.symmetries.get(self.name)["period"] = nper
                return values
            elif "period" in self.symmetries.get(self.name):
                return values
            else:
                raise AxisError("ERROR: unknown periodicity")
        else:
            return values
    else:
        if self.name in self.symmetries:
            values = rebuild_symmetries_axis(values, self.symmetries.get(self.name))
            return values
        else:
            return values
