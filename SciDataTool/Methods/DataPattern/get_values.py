from importlib import import_module
from numpy import array

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
    operation=None,
    is_real=True,
    corr_unit=None,
    is_full=False,
):
    """Returns the vector 'axis' taking symmetries into account.
    Parameters
    ----------
    self: DataPattern
        a DataPattern object
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
    operation: str
        name of the operation (e.g. "freqs_to_time")
    Returns
    -------
    Vector of axis values
    """
    values = self.values

    # Rebuild pattern
    if is_smallestperiod or is_pattern:
        pass
    else:
        if self.values_whole is not None:
            values = self.values_whole
        else:
            values = values[self.rebuild_indices]

    # fft/ifft
    if operation is not None:
        module = import_module("SciDataTool.Functions.conversions")
        func = getattr(module, operation)  # Conversion function
        values = array(func(values, is_real=is_real))

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
                # Axis is in the correct unit for the normalization
                values = self.normalizations[normalization].normalize(values)
            else:
                raise NormError("Normalization is not available in this unit")
        else:
            raise NormError("Normalization is not available")

    # Unit conversion
    if unit != "SI" and unit != self.unit:
        if corr_unit is not None:
            values = convert(values, corr_unit, unit)
        else:
            values = convert(values, self.unit, unit)

    return values
