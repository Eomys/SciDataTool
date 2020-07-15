# -*- coding: utf-8 -*-

from numpy import zeros

from SciDataTool.Functions.conversions import xy_to_rphi, cart2pol
from SciDataTool.Functions import AxisError


def get_harm_rphiz_along(self, N_harm, *args, unit="SI", is_norm=False, axis_data=[]):
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
        
    if "x" in self.components.keys() and "y" in self.components.keys():
        # Extract from DataND
        resultx = self.components["x"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        resulty = self.components["y"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        field_x = resultx[self.components["x"].symbol]
        field_y = resulty[self.components["y"].symbol]
        shape = field_x.shape
        x = resultx["x"]
        y = resultx["y"]
        # Convert to cylindrical coordinates
        (r, phi) = xy_to_rphi(x, y)
        (field_r, field_t) = cart2pol(field_x, field_y, phi)
        if "axial" in self.components.keys():
            resultz = self.components["axial"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_z = resultz[self.components["axial"].symbol]
        elif "z" in self.components.keys():
            resultz = self.components["z"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_z = resultz[self.components["z"].symbol]
        else:
            field_z = zeros(shape)
        return_dict = dict(resultx)
        del return_dict[self.components["x"].symbol]
        
    elif "radial" in self.components.keys():
        resultr = self.components["radial"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        field_r = resultr[self.components["radial"].symbol]
        shape = field_r.shape
        if "tangential" in self.components.keys():
            resultphi = self.components["tangential"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_t = resultphi[self.components["tangential"].symbol]
        else:
            field_t = zeros(shape)
        if "axial" in self.components.keys():
            resultz = self.components["axial"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_z = resultz[self.components["axial"].symbol]
        elif "z" in self.components.keys():
            resultz = self.components["z"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_z = resultz[self.components["z"].symbol]
        else:
            field_z = zeros(shape)
        return_dict = dict(resultr)
        del return_dict[self.components["radial"].symbol]
        
    elif "tangential" in self.components.keys():
        resultphi = self.components["tangential"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        field_t = resultphi[self.components["tangential"].symbol]
        shape = field_t.shape
        if "radial" in self.components.keys():
            resultr = self.components["radial"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_r = resultphi[self.components["radial"].symbol]
        else:
            field_r = zeros(shape)
        if "axial" in self.components.keys():
            resultz = self.components["axial"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_z = resultz[self.components["axial"].symbol]
        elif "z" in self.components.keys():
            resultz = self.components["z"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
            field_z = resultz[self.components["z"].symbol]
        else:
            field_z = zeros(shape)
        return_dict = dict(resultphi)
        del return_dict[self.components["tangential"].symbol]
        
    elif "axial" in self.components.keys():
        resultz = self.components["axial"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        field_z = resultz[self.components["axial"].symbol]
        shape = field_z.shape
        field_r = zeros(shape)
        field_t = zeros(shape)
        return_dict = dict(resultz)
        del return_dict[self.components["axial"].symbol]
    
    elif "z" in self.components.keys():
        resultz = self.components["z"].get_harmonics(N_harm, args, unit=unit, is_norm=is_norm, axis_data=axis_data)
        field_z = resultz[self.components["z"].symbol]
        shape = field_z.shape
        field_r = zeros(shape)
        field_t = zeros(shape)
        return_dict = resultz
        del return_dict[self.components["z"].symbol]
        
    else:
        raise AxisError("Vector_field object is empty (should contain at least radial, tangential, axial, x, y or z")
        
    return_dict[self.symbol + "_r"] = field_r
    return_dict[self.symbol + "_t"] = field_t
    return_dict[self.symbol + "_z"] = field_z
        
    return return_dict
    
