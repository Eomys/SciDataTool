# -*- coding: utf-8 -*-

from SciDataTool.Functions.conversions import xy_to_rphi, cart2pol
from SciDataTool.Functions import AxisError


def get_mag_tan_along(self, *args, unit="SI", is_norm=False, axis_data=[]):
    """Returns the ndarray of the tangential component of the field, using conversions and symmetries if needed.
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
    list of 1Darray of axes values, ndarray of field values
    """
    
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args
        
    if "tangential" in self.components.keys():
        return_dict = self.components["tangential"].get_magnitude_along(args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        return_dict[self.symbol + "_t"] = return_dict.pop(self.components["tangential"].symbol)
        
    elif "x" in self.components.keys() and "y" in self.components.keys():
        # Extract from DataND
        resultx = self.components["x"].get_magnitude_along(args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        resulty = self.components["y"].get_magnitude_along(args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        field_x = resultx[self.components["x"].symbol]
        field_y = resulty[self.components["y"].symbol]
        x = resultx["x"]
        y = resultx["y"]
        # Convert to cylindrical coordinates
        (r, phi) = xy_to_rphi(x, y)
        (field_r, field_t) = cart2pol(field_x, field_y, phi)
        return_dict = dict(resultx)
        del return_dict[self.components["x"].symbol]
        return_dict[self.symbol + "_t"] = field_t
    else:
        raise AxisError("tangential or x,y components necessary")
        
    return return_dict
    
