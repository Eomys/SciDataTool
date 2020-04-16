# -*- coding: utf-8 -*-
"""File generated according to SciDataTool/Generator/ClassesRef/Output/Data1D.csv
WARNING! All changes made in this file will be lost!
"""
from os import linesep
from SciDataTool.Classes._check import set_array, check_init_dict, check_var, raise_
from SciDataTool.Functions.save import save
from SciDataTool.Classes.Data import Data

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from SciDataTool.Methods.Data1D.get_values import get_values
except ImportError as error:
    get_values = error
from numpy import array, array_equal, squeeze
from SciDataTool.Classes._check import InitUnKnowClassError


class Data1D(Data):
    """Abstract class for all kinds of data"""

    VERSION = 1
    # cf Methods.Data1D.get_values
    if isinstance(get_values, ImportError):
        get_values = property(
            fget=lambda x: raise_(
                ImportError("Can't use Data1D method get_values: " + str(get_values))
            )
        )
    else:
        get_values = get_values
    # save method is available in all object
    save = save

    def __init__(
        self, values=[], symbol="", name="", unit="", symmetries={}, init_dict=None,
    ):
        """Constructor of the class. Can be use in two ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for SciDataTool type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary wiht every properties as keys
        ndarray or list can be given for Vector and Matrix
        object or dict can be given for SciDataTool Object"""
        if init_dict is not None:  # Initialisation by dict
            check_init_dict(
                init_dict, ["values", "symbol", "name", "unit", "symmetries"]
            )
            # Overwrite default value with init_dict content
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
        # Initialisation by argument
        # values can be None, a ndarray or a list
        set_array(self, "values", values)
        # Call Data init
        super(Data1D, self).__init__(
            symbol=symbol, name=name, unit=unit, symmetries=symmetries
        )
        # The class is frozen (in Data init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""
        Data1D_str = ""
        # Get the properties inherited from Data
        Data1D_str += super(Data1D, self).__str__() + linesep
        Data1D_str += "values = " + linesep + str(self.values)
        return Data1D_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""
        if type(other) != type(self):
            return False
        # Check the properties inherited from Data
        if not super(Data1D, self).__eq__(other):
            return False
        if not array_equal(other.values, self.values):
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """
        # Get the properties inherited from Data
        Data1D_dict = super(Data1D, self).as_dict()
        if self.values is None:
            Data1D_dict["values"] = None
        else:
            Data1D_dict["values"] = self.values.tolist()
        # The class name is added to the dict fordeserialisation purpose
        # Overwrite the mother class name
        Data1D_dict["__class__"] = "Data1D"
        return Data1D_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""
        self.values = None
        # Set to None the properties inherited from Data
        super(Data1D, self)._set_None()

    def _get_values(self):
        """getter of values"""
        return self._values

    def _set_values(self, value):
        """setter of values"""
        if type(value) is list:
            try:
                value = squeeze(array(value))
            except:
                value = squeeze(value)
        check_var("values", value, "ndarray")
        self._values = value

    # ndarray of the field
    # Type : ndarray
    values = property(
        fget=_get_values, fset=_set_values, doc=u"""ndarray of the field"""
    )
