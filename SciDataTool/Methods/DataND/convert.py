# -*- coding: utf-8 -*-
from SciDataTool.Functions import NormError
from SciDataTool.Functions.conversions import convert as convert_unit


def convert(self, values, unit, is_norm):
    """Returns the values of the field transformed or converted.
    Parameters
    ----------
    self: Data
        a Data object
    values: ndarray
        array of the field
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    Returns
    -------
    values: ndarray
        values of the field
    """

    # Convert into right unit
    if unit == self.unit or unit == "SI":
        if is_norm:
            try:
                values = values / self.normalizations.get("ref")
            except:
                raise NormError(
                    "ERROR: Reference value not specified for normalization"
                )
    elif unit in self.normalizations:
        values = values / self.normalizations.get(unit)
    else:
        values = convert_unit(values, self.unit, unit)
    return values
