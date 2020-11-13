# -*- coding: utf-8 -*-

from numpy import zeros

from SciDataTool.Functions.conversions import xy_to_rphi, cart2pol
from SciDataTool.Functions import AxisError


def get_rphiz_along(self, *args, unit="SI", is_norm=False, axis_data=[]):
    """Returns the list of the cylindrical (r,phi,z) components of the field, using conversions and symmetries if needed.
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

    if "comp_x" in self.components.keys() and "comp_y" in self.components.keys():
        # Extract from DataND
        resultx = self.components["comp_x"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        resulty = self.components["comp_y"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_x = resultx[self.components["comp_x"].symbol]
        field_y = resulty[self.components["comp_y"].symbol]
        shape = field_x.shape
        if "phi" not in resultx:
            raise AxisError(
                "ERROR: need phi axis to convert to cylindircal coordinates"
            )
        phi = resultx["phi"]
        # Convert to cylindrical coordinates
        (field_r, field_c) = cart2pol(field_x, field_y, phi)
        if "axial" in self.components.keys():
            resultz = self.components["axial"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_z = resultz[self.components["axial"].symbol]
        elif "comp_z" in self.components.keys():
            resultz = self.components["comp_z"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_z = resultz[self.components["comp_z"].symbol]
        else:
            field_z = zeros(shape)
        return_dict = dict(resultx)
        del return_dict[self.components["comp_x"].symbol]

    elif "radial" in self.components.keys():
        resultr = self.components["radial"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_r = resultr[self.components["radial"].symbol]
        shape = field_r.shape
        if "tangential" in self.components.keys():
            resultphi = self.components["tangential"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_c = resultphi[self.components["tangential"].symbol]
        else:
            field_c = zeros(shape)
        if "axial" in self.components.keys():
            resultz = self.components["axial"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_z = resultz[self.components["axial"].symbol]
        elif "comp_z" in self.components.keys():
            resultz = self.components["comp_z"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_z = resultz[self.components["comp_z"].symbol]
        else:
            field_z = zeros(shape)
        return_dict = dict(resultr)
        del return_dict[self.components["radial"].symbol]

    elif "tangential" in self.components.keys():
        resultphi = self.components["circumferential"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_c = resultphi[self.components["tangential"].symbol]
        shape = field_c.shape
        if "radial" in self.components.keys():
            resultr = self.components["radial"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_r = resultphi[self.components["radial"].symbol]
        else:
            field_r = zeros(shape)
        if "axial" in self.components.keys():
            resultz = self.components["axial"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_z = resultz[self.components["axial"].symbol]
        elif "comp_z" in self.components.keys():
            resultz = self.components["comp_z"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_z = resultz[self.components["comp_z"].symbol]
        else:
            field_z = zeros(shape)
        return_dict = dict(resultphi)
        del return_dict[self.components["tangential"].symbol]

    elif "axial" in self.components.keys():
        resultz = self.components["axial"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_z = resultz[self.components["axial"].symbol]
        shape = field_z.shape
        field_r = zeros(shape)
        field_c = zeros(shape)
        return_dict = dict(resultz)
        del return_dict[self.components["axial"].symbol]

    elif "comp_z" in self.components.keys():
        resultz = self.components["comp_z"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_z = resultz[self.components["comp_z"].symbol]
        shape = field_z.shape
        field_r = zeros(shape)
        field_c = zeros(shape)
        return_dict = resultz
        del return_dict[self.components["comp_z"].symbol]

    else:
        raise AxisError(
            "Vector_field object is empty (should contain at least radial, circumferential, axial, x, y or z"
        )

    return_dict["radial"] = field_r
    return_dict["tangential"] = field_c
    return_dict["axial"] = field_z

    return return_dict
