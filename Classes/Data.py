# -*- coding: utf-8 -*-
"""File generated according to pyleecan/Generator/ClassesRef/Output/Data.csv
WARNING! All changes made in this file will be lost!
"""

from os import linesep
from pyleecan.Classes._check import check_init_dict, check_var, raise_
from pyleecan.Functions.save import save
from pyleecan.Classes._frozen import FrozenClass

from pyleecan.Classes._check import InitUnKnowClassError


class Data(FrozenClass):
    """Abstract class for all kinds of data"""

    VERSION = 1

    # save method is available in all object
    save = save

    def __init__(
        self, symbol=None, name=None, unit=None, symmetries=None, init_dict=None
    ):
        """Constructor of the class. Can be use in two ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for pyleecan type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary wiht every properties as keys

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if init_dict is not None:  # Initialisation by dict
            check_init_dict(init_dict, ["symbol", "name", "unit", "symmetries"])
            # Overwrite default value with init_dict content
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
        # Initialisation by argument
        self.parent = None
        self.symbol = symbol
        self.name = name
        self.unit = unit
        self.symmetries = symmetries

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        Data_str = ""
        if self.parent is None:
            Data_str += "parent = None " + linesep
        else:
            Data_str += "parent = " + str(type(self.parent)) + " object" + linesep
        Data_str += 'symbol = "' + str(self.symbol) + '"' + linesep
        Data_str += 'name = "' + str(self.name) + '"' + linesep
        Data_str += 'unit = "' + str(self.unit) + '"' + linesep
        Data_str += "symmetries = " + str(self.symmetries)
        return Data_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.symbol != self.symbol:
            return False
        if other.name != self.name:
            return False
        if other.unit != self.unit:
            return False
        if other.symmetries != self.symmetries:
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        Data_dict = dict()
        Data_dict["symbol"] = self.symbol
        Data_dict["name"] = self.name
        Data_dict["unit"] = self.unit
        Data_dict["symmetries"] = self.symmetries
        # The class name is added to the dict fordeserialisation purpose
        Data_dict["__class__"] = "Data"
        return Data_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.symbol = None
        self.name = None
        self.unit = None
        self.symmetries = None

    def _get_symbol(self):
        """getter of symbol"""
        return self._symbol

    def _set_symbol(self, value):
        """setter of symbol"""
        check_var("symbol", value, "str")
        self._symbol = value

    # Symbol of the variable (in latex syntax)
    # Type : str
    symbol = property(
        fget=_get_symbol,
        fset=_set_symbol,
        doc=u"""Symbol of the variable (in latex syntax)""",
    )

    def _get_name(self):
        """getter of name"""
        return self._name

    def _set_name(self, value):
        """setter of name"""
        check_var("name", value, "str")
        self._name = value

    # Name of the physical quantity (to be used in plots)
    # Type : str
    name = property(
        fget=_get_name,
        fset=_set_name,
        doc=u"""Name of the physical quantity (to be used in plots)""",
    )

    def _get_unit(self):
        """getter of unit"""
        return self._unit

    def _set_unit(self, value):
        """setter of unit"""
        check_var("unit", value, "str")
        self._unit = value

    # Unit of the physical quantity (to be used in plots)
    # Type : str
    unit = property(
        fget=_get_unit,
        fset=_set_unit,
        doc=u"""Unit of the physical quantity (to be used in plots)""",
    )

    def _get_symmetries(self):
        """getter of symmetries"""
        return self._symmetries

    def _set_symmetries(self, value):
        """setter of symmetries"""
        check_var("symmetries", value, "dict")
        self._symmetries = value

    # List of the symmetries along each axis used for reducing storage
    # Type : dict
    symmetries = property(
        fget=_get_symmetries,
        fset=_set_symmetries,
        doc=u"""List of the symmetries along each axis used for reducing storage""",
    )
