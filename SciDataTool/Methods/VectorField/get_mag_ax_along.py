# -*- coding: utf-8 -*-

from SciDataTool.Functions import AxisError


def get_mag_ax_along(self, *args, unit="SI", is_norm=False, axis_data=[]):
    """Returns the ndarray of the axial (z) component of the field, using conversions and symmetries if needed.
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

    if "axial" in self.components.keys():
        return_dict = self.components["axial"].get_magnitude_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        return_dict[self.symbol + "_z"] = return_dict.pop(
            self.components["axial"].symbol
        )

    elif "z" in self.components.keys():
        return_dict = self.components["z"].get_magnitude_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        return_dict[self.symbol + "_z"] = return_dict.pop(self.components["z"].symbol)

    else:
        raise AxisError("axial or z component necessary")

    return return_dict
