# -*- coding: utf-8 -*-
from SciDataTool.Functions.conversions import convert


def get_values(
    self,
    unit="SI",
    is_pattern=False,
    is_oneperiod=False,
    is_antiperiod=False,
    is_smallestperiod=False,
):
    """Returns the vector 'axis' taking symmetries into account.
    Parameters
    ----------
    self: DataPattern
        a DataPattern object
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

    # Rebuild pattern
    if is_smallestperiod or is_pattern:
        return values
    else:
        if self.values_whole is not None:
            return self.values_whole
        else:
            return values[self.rebuild_indices]
