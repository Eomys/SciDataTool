# -*- coding: utf-8 -*-
"""File generated according to SciDataTool/Generator/ClassesRef/Output/Data.csv
WARNING! All changes made in this file will be lost!
"""
from os import linesep
from numpy import squeeze, array
from SciDataTool.Classes._check import check_init_dict, check_var, raise_
from SciDataTool.Functions.save import save
from SciDataTool.Classes._frozen import FrozenClass
from SciDataTool.Classes._check import InitUnKnowClassError

try:
    from SciDataTool.Methods.RequestedAxis.get_axis import get_axis
except ImportError as error:
    get_axis = error

class RequestedAxis(FrozenClass):
    """Class for handling of requested axis during get_along methods"""

    VERSION = 1
    # cf Methods.DataND.get_axis
    if isinstance(get_axis, ImportError):
        get_axis = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use RequestedAxis method get_axis: " + str(get_axis)
                )
            )
        )
    else:
        get_axis = get_axis
    # save method is available in all object
    save = save

    def __init__(
        self, name="", 
        corr_name="", 
        unit="", 
        extension="", 
        values=None, 
        indices=None, 
        input_data=None, 
        operation=None, 
        index=None,
        transform=None,
    ):
        """Constructor of the class. Can be use in two ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for SciDataTool type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary wiht every properties as keys
        ndarray or list can be given for Vector and Matrix
        object or dict can be given for SciDataTool Object"""
        # Initialisation by argument
        self.name = name
        self.corr_name = corr_name
        self.unit = unit
        self.extension = extension
        self.values = values
        self.indices = indices
        self.input_data = input_data
        self.operation = operation
        self.index = index
        self.transform = transform

#    def _get_name(self):
#        """getter of name"""
#        return self.name
#    def _set_name(self, value):
#        """setter of name"""
#        check_var("name", value, "str")
#        self._name = value
#    # Type : str
#    name = property(
#        fget=_get_name,
#        fset=_set_name,
#    )
#    
#    def _get_corr_name(self):
#        """getter of corr_name"""
#        return self.corr_name
#    def _set_corr_name(self, value):
#        """setter of corr_name"""
#        check_var("corr_name", value, "str")
#        self._corr_name = value
#    # Type : str
#    corr_name = property(
#        fget=_get_corr_name,
#        fset=_set_corr_name,
#    )
#    
#    def _get_unit(self):
#        """getter of unit"""
#        return self.unit
#    def _set_unit(self, value):
#        """setter of unit"""
#        check_var("unit", value, "str")
#        self._unit = value
#    # Type : str
#    unit = property(
#        fget=_get_unit,
#        fset=_set_unit,
#    )
#    
#    def _get_extension(self):
#        """getter of extension"""
#        return self.extension
#    def _set_extension(self, value):
#        """setter of extension"""
#        check_var("extension", value, "str")
#        self._extension = value
#    # Type : str
#    extension = property(
#        fget=_get_extension,
#        fset=_set_extension,
#    )
#    
#    def _get_values(self):
#        """getter of values"""
#        return self.values
#    def _set_values(self, value):
#        """setter of values"""
#        check_var("values", value, "ndarray")
#        self._values = value
#    # Type : str
#    values = property(
#        fget=_get_values,
#        fset=_set_values,
#    )
#    
#    def _get_indices(self):
#        """getter of indices"""
#        return self.indices
#    def _set_indices(self, value):
#        """setter of indices"""
#        check_var("indices", value, "ndarray")
#        self._indices = value
#    # Type : str
#    indices = property(
#        fget=_get_indices,
#        fset=_set_indices,
#    )
#    
#    def _get_input_data(self):
#        """getter of input_data"""
#        return self.input_data
#    def _set_input_data(self, value):
#        """setter of input_data"""
#        if type(value) is list:
#            try:
#                value = squeeze(array(value))
#            except:
#                value = squeeze(value)
#        check_var("input_data", value, "ndarray")
#        self._input_data = value
#    # Type : str
#    input_data = property(
#        fget=_get_input_data,
#        fset=_set_input_data,
#    )
#    
#    def _get_operation(self):
#        """getter of operation"""
#        return self.operation
#    def _set_operation(self, value):
#        """setter of operation"""
#        check_var("operation", value, "str")
#        self._operation = value
#    # Type : str
#    operation = property(
#        fget=_get_operation,
#        fset=_set_operation,
#    )
