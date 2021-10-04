from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from SciDataTool.Functions import AxisError, NormError


def get_values(
    self,
    unit="SI",
    is_oneperiod=False,
    is_antiperiod=False,
    is_smallestperiod=False,
    normalization=None,
):
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
    is_smallestperiod: bool
        return values on smallest available period
    normalization: str
        name of normalization to use
    Returns
    -------
    Vector of axis values
    """
    values = self.values

    if unit != "SI" and unit != self.unit:
        if unit in self.normalizations and normalization is None:
            normalization = unit
            unit = "SI"

    # Normalization
    if normalization is not None:
        if normalization in self.normalizations:
            if (
                self.normalizations[normalization].unit == "SI"
                or self.normalizations[normalization].unit == self.unit
            ):
                # Axis is int he correct unit for the normalization
                values = self.normalizations[normalization].normalize(values)
            else:
                raise NormError("Normalization is not available in this unit")
        else:
            raise NormError("Normalization is not available")

    # Unit conversion
    if unit != "SI" and unit != self.unit:
        values = convert(values, self.unit, unit)

    # Ignore symmetries if fft axis
    if self.name == "freqs" or self.name == "wavenumber":
        is_smallestperiod = True

    # Rebuild symmetries
    if is_smallestperiod:
        return values
    elif is_antiperiod:
        if "antiperiod" in self.symmetries:
            return values
        else:
            raise AxisError("ERROR: axis has no antiperiodicity")
    elif is_oneperiod:
        if "antiperiod" in self.symmetries:
            nper = self.symmetries["antiperiod"]
            self.symmetries["antiperiod"] = 2
            values = rebuild_symmetries_axis(values, self.symmetries)
            self.symmetries["antiperiod"] = nper
            return values
        elif "period" in self.symmetries:
            return values
        else:
            return values
    else:
        values = rebuild_symmetries_axis(values, self.symmetries)
        return values
