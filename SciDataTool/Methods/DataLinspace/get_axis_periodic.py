from SciDataTool.Functions import AxisError


def get_axis_periodic(self, Nper, is_aper=False):
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
    New_axis: DataLinspace
        Axis with requested (anti-)periodicities
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataLinspace", fromlist=["DataLinspace"])
    DataLinspace = getattr(module, "DataLinspace")

    try:
        # Reduce axis to the given periodicity
        Nper = Nper * 2 if is_aper else Nper
        values = self.get_values()
        N = self.get_length()

        if N % Nper != 0:
            raise AxisError("length of axis is not divisible by the number of periods")
        values_per = values[: int(N / Nper)]

        if is_aper:
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
            is_components=self.is_components,
            symbol=self.symbol,
        )

    except AxisError:
        # Periodicity cannot be applied, return full axis
        New_axis = self.copy()

    return New_axis
