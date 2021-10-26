from SciDataTool.Functions import NormError
from SciDataTool.Functions.conversions import convert
from numpy import angle as np_angle


def get_phase_along(self, *args, unit="SI", is_norm=False, axis_data=[]):
    """Returns the ndarray of the magnitude of the FT, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    axis_data: list
        list of ndarray corresponding to user-input data
    Returns
    -------
    list of 1Darray of axes values, ndarray of magnitude values
    """
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args
    return_dict = self.get_along(args, axis_data=axis_data)
    values = return_dict[self.symbol]
    # Compute magnitude
    values = np_angle(values)
    # Convert into right unit (apart because of degree conversion)
    if unit == self.unit or unit == "SI":
        if is_norm:
            try:
                values = self.normalizations["ref"].normalize(values)
            except:
                raise NormError("Reference value not specified for normalization")
    elif unit == "°":
        values = convert(values, "rad", "°")
    elif unit in self.normalizations:
        values = self.normalizations.get(unit).normalize(values)
    else:
        values = convert(values, self.unit, unit)
    return_dict[self.symbol] = values
    return return_dict
