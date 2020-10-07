# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from SciDataTool.Functions import AxisError


def get_values(self, unit="SI", is_oneperiod=False, is_antiperiod=False):
    """Returns the vector 'axis' taking symmetries into account.
    Parameters
    ----------
    self: Data1D
        a Data1D object
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
    values = self.values

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
                self.symmetries.get(self.name)["antiperiod"] = nper
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
