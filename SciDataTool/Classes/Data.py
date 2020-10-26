# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Data.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//Data
"""

from os import linesep
from logging import getLogger
from ._check import check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from ._frozen import FrozenClass

from ._check import InitUnKnowClassError


class Data(FrozenClass):
    """Abstract class for all kinds of data"""

    VERSION = 1

    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self,
        symbol="",
        name="",
        unit="",
        normalizations=-1,
        init_dict=None,
        init_str=None,
    ):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for SciDataTool type, -1 will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with property names as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for SciDataTool Object"""

        if init_str is not None:  # Load from a file
            init_dict = load_init_dict(init_str)[1]
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "normalizations" in list(init_dict.keys()):
                normalizations = init_dict["normalizations"]
        # Set the properties (value check and convertion are done in setter)
        self.parent = None
        self.symbol = symbol
        self.name = name
        self.unit = unit
        self.normalizations = normalizations

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        Data_str = ""
        if self.parent is None:
            Data_str += "parent = None " + linesep
        else:
            Data_str += "parent = " + str(type(self.parent)) + " object" + linesep
        Data_str += 'symbol = "' + str(self.symbol) + '"' + linesep
        Data_str += 'name = "' + str(self.name) + '"' + linesep
        Data_str += 'unit = "' + str(self.unit) + '"' + linesep
        Data_str += "normalizations = " + str(self.normalizations) + linesep
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
        if other.normalizations != self.normalizations:
            return False
        return True

    def as_dict(self):
        """Convert this object in a json seriable dict (can be use in __init__)"""

        Data_dict = dict()
        Data_dict["symbol"] = self.symbol
        Data_dict["name"] = self.name
        Data_dict["unit"] = self.unit
        Data_dict["normalizations"] = (
            self.normalizations.copy() if self.normalizations is not None else None
        )
        # The class name is added to the dict for deserialisation purpose
        Data_dict["__class__"] = "Data"
        return Data_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.symbol = None
        self.name = None
        self.unit = None
        self.normalizations = None

    def _get_symbol(self):
        """getter of symbol"""
        return self._symbol

    def _set_symbol(self, value):
        """setter of symbol"""
        check_var("symbol", value, "str")
        self._symbol = value

    symbol = property(
        fget=_get_symbol,
        fset=_set_symbol,
        doc=u"""Symbol of the variable (in latex syntax)

        :Type: str
        """,
    )

    def _get_name(self):
        """getter of name"""
        return self._name

    def _set_name(self, value):
        """setter of name"""
        check_var("name", value, "str")
        self._name = value

    name = property(
        fget=_get_name,
        fset=_set_name,
        doc=u"""Name of the physical quantity (to be used in plots)

        :Type: str
        """,
    )

    def _get_unit(self):
        """getter of unit"""
        return self._unit

    def _set_unit(self, value):
        """setter of unit"""
        check_var("unit", value, "str")
        self._unit = value

    unit = property(
        fget=_get_unit,
        fset=_set_unit,
        doc=u"""Unit of the physical quantity (to be used in plots)

        :Type: str
        """,
    )

    def _get_normalizations(self):
        """getter of normalizations"""
        return self._normalizations

    def _set_normalizations(self, value):
        """setter of normalizations"""
        if type(value) is int and value == -1:
            value = dict()
        check_var("normalizations", value, "dict")
        self._normalizations = value

    normalizations = property(
        fget=_get_normalizations,
        fset=_set_normalizations,
        doc=u"""Normalizations available for the field and its axes

        :Type: dict
        """,
    )
