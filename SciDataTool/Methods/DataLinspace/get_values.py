from importlib import import_module
from numpy import array

from SciDataTool.Functions.conversions import convert
from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from SciDataTool.Functions import AxisError, NormError
from numpy import linspace


def get_values(
    self,
    unit="SI",
    is_oneperiod=False,
    is_antiperiod=False,
    is_smallestperiod=False,
    normalization=None,
    operation=None,
    is_real=True,
    corr_unit=None,
):
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
    is_smallestperiod: bool
        return values on smallest available period
    normalization: str
        name of normalization to use
    operation: str
        name of the operation (e.g. "freqs_to_time")
    Returns
    -------
    Vector of axis values
    """
    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.Norm_vector", fromlist=["Norm_vector"])
    Norm_vector = getattr(module, "Norm_vector")

    if unit != "SI" and unit != self.unit:
        if unit in self.normalizations and normalization is None:
            normalization = unit
            unit = "SI"

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

    norm_vector = None

    # Ignore symmetries if fft axis
    if self.name == "freqs" or self.name == "wavenumber":
        is_smallestperiod = True

    # Rebuild symmetries
    if is_smallestperiod:
        pass
    elif is_antiperiod:
        if "antiperiod" in self.symmetries:
            pass
        else:
            raise AxisError("axis has no antiperiodicity")
    elif is_oneperiod:
        if "antiperiod" in self.symmetries:
            nper = self.symmetries["antiperiod"]
            self.symmetries["antiperiod"] = 2
            values = rebuild_symmetries_axis(values, self.symmetries)
            self.symmetries["antiperiod"] = nper
            pass
        elif "period" in self.symmetries:
            pass
        else:
            pass
    else:
        values = rebuild_symmetries_axis(values, self.symmetries)
        if (
            normalization is not None
            and normalization in self.normalizations
            and isinstance(self.normalizations[normalization], Norm_vector)
        ):
            norm_vector = self.normalizations[normalization].vector.copy()
            self.normalizations[normalization].vector = rebuild_symmetries_axis(
                norm_vector, self.symmetries
            )

    # fft/ifft
    if operation is not None:
        module = import_module("SciDataTool.Functions.conversions")
        func = getattr(module, operation)  # Conversion function
        values = array(func(values, is_real=is_real))

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

    if norm_vector is not None:
        self.normalizations[normalization].vector = norm_vector

    return values
