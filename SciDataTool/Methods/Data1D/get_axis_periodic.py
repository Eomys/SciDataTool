# -*- coding: utf-8 -*-
from SciDataTool.Functions import AxisError


def get_axis_periodic(self, Nper, is_antiperiod=False):
    """Returns the vector 'axis' taking symmetries into account.
    Parameters
    ----------
    self: Data1D
        a Data1D object
    Nper: int
        number of periods
    is_antiperiod: bool
        return values on a semi period (only for antiperiodic signals)
    Returns
    -------
    New Data1D
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.Data1D", fromlist=["Data1D"])
    Data1D = getattr(module, "Data1D")

    values = self.values
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

    New_axis = Data1D(
        values=values_per,
        name=self.name,
        unit=self.unit,
        symmetries={sym: Nper},
        is_components=self.is_components,
        symbol=self.symbol,
    )

    return New_axis
