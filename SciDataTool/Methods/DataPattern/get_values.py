from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions import NormError


def get_values(
    self,
    unit="SI",
    is_oneperiod=False,
    is_antiperiod=False,
    is_smallestperiod=False,
    is_pattern=False,
    normalization=None,
):
    """Returns the vector 'axis' taking symmetries into account.
    Parameters
    ----------
    self: DataLinspace
        a DataLinspace object
    unit: str
        requested unit
    is_oneperiod: bool
        return values on a single period (unused here)
    is_antiperiod: bool
        return values on a semi period (unused here)
    is_smallestperiod: bool
        return values on smallest available period (pattern here => is_pattern)
    is_pattern: bool
        return values on smallest available pattern
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

    # Rebuild pattern
    if is_smallestperiod or is_pattern:
        return values
    else:
        if self.values_whole is not None:
            return self.values_whole
        else:
            return values[self.rebuild_indices]
