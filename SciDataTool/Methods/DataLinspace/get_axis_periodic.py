# -*- coding: utf-8 -*-
from SciDataTool.Functions import AxisError


def get_axis_periodic(self, Nper, is_antiperiod=False):
    """Returns the vector 'axis' taking symmetries into account.
    Parameters
    ----------
    self: DataLinspace
        a DataLinspace object
    Nper: int
        number of periods
    is_antiperiod: bool
        return values on a semi period (only for antiperiodic signals)
    Returns
    -------
    New DataLinspace
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataLinspace", fromlist=["DataLinspace"])
    DataLinspace = getattr(module, "DataLinspace")

    values = self.get_values()
    N = self.get_length()

    if N % Nper != 0:
        raise AxisError(
            "ERROR: length of axis is not divisible by the number of periods"
        )

    values_per = values[: int(N / Nper)]

    if is_antiperiod:
        sym = "antiperiod"
    else:
        sym = "period"

    New_axis = DataLinspace(
        initial=self.initial,
        final=values_per[-1],
        number=int(N / Nper),
        include_endpoint=True,
        name=self.name,
        unit=self.unit,
        symmetries={sym: Nper},
        normalizations=self.normalizations,
        is_str=self.is_str,
        symbol=self.symbol,
    )

    return New_axis
