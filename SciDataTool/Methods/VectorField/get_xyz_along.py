# -*- coding: utf-8 -*-

from numpy import zeros

from SciDataTool.Functions.conversions import pol2cart
from SciDataTool.Functions import AxisError


def get_xyz_along(self, *args, unit="SI", is_norm=False, axis_data=[]):
    """Returns the list of the cartesian (comp_x,comp_y,comp_z) components of the field, using conversions and symmetries if needed.
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

    if "radial" in self.components.keys() and "tangential" in self.components.keys():
        # Extract from DataND
        resultr = self.components["radial"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        resultphi = self.components["tangential"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_r = resultr[self.components["radial"].symbol]
        field_c = resultphi[self.components["tangential"].symbol]
        shape = field_r.shape
        if "angle" not in resultr:
            raise AxisError(
                "ERROR: need angle axis to convert to cartesian coordinates"
            )
        phi = resultr["angle"]
        # Convert to cylindrical coordinates
        (field_x, field_y) = pol2cart(field_r, field_c, phi)
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

    elif "comp_x" in self.components.keys():
        resultx = self.components["comp_x"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_x = resultx[self.components["comp_x"].symbol]
        shape = field_x.shape
        if "comp_y" in self.components.keys():
            resulty = self.components["comp_y"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_y = resulty[self.components["comp_y"].symbol]
        else:
            field_y = zeros(shape)
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

    elif "comp_y" in self.components.keys():
        resulty = self.components["comp_y"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_y = resultphi[self.components["comp_y"].symbol]
        shape = field_y.shape
        if "comp_x" in self.components.keys():
            resultx = self.components["comp_x"].get_along(
                args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
            field_x = resultphi[self.components["comp_x"].symbol]
        else:
            field_x = zeros(shape)
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
        return_dict = dict(resulty)
        del return_dict[self.components["comp_y"].symbol]

    elif "axial" in self.components.keys():
        resultz = self.components["axial"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_z = resultz[self.components["axial"].symbol]
        shape = field_z.shape
        field_x = zeros(shape)
        field_y = zeros(shape)
        return_dict = dict(resultz)
        del return_dict[self.components["axial"].symbol]

    elif "comp_z" in self.components.keys():
        resultz = self.components["comp_z"].get_along(
            args, unit=unit, is_norm=is_norm, axis_data=axis_data
        )
        field_z = resultz[self.components["comp_z"].symbol]
        shape = field_z.shape
        field_x = zeros(shape)
        field_y = zeros(shape)
        return_dict = resultz
        del return_dict[self.components["comp_z"].symbol]

    else:
        raise AxisError(
            "Vector_field object is empty (should contain at least radial, tangential, axial, x, y or z"
        )

    return_dict["comp_x"] = field_x
    return_dict["comp_y"] = field_y
    return_dict["comp_z"] = field_z

    return return_dict
