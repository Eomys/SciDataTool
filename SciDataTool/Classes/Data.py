# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Data.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//Data
"""

from os import linesep
from sys import getsizeof
from ._check import check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from ._frozen import FrozenClass

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Data._set_normalizations import _set_normalizations
except ImportError as error:
    _set_normalizations = error


from ._check import InitUnKnowClassError


class Data(FrozenClass):
    """Abstract class for all kinds of data"""

    VERSION = 1

    # cf Methods.Data._set_normalizations
    if isinstance(_set_normalizations, ImportError):
        _set_normalizations = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Data method _set_normalizations: "
                    + str(_set_normalizations)
                )
            )
        )
    else:
        _set_normalizations = _set_normalizations
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
        - __init__ (init_dict = d) d must be a dictionary with property names as keys
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
        if len(self.normalizations) == 0:
            Data_str += "normalizations = dict()" + linesep
        for key, obj in self.normalizations.items():
            tmp = (
                self.normalizations[key].__str__().replace(linesep, linesep + "\t")
                + linesep
            )
            Data_str += "normalizations[" + key + "] =" + tmp + linesep + linesep
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

    def compare(self, other, name="self", ignore_list=None):
        """Compare two objects and return list of differences"""

        if ignore_list is None:
            ignore_list = list()
        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()
        if other._symbol != self._symbol:
            diff_list.append(name + ".symbol")
        if other._name != self._name:
            diff_list.append(name + ".name")
        if other._unit != self._unit:
            diff_list.append(name + ".unit")
        if (other.normalizations is None and self.normalizations is not None) or (
            other.normalizations is not None and self.normalizations is None
        ):
            diff_list.append(name + ".normalizations None mismatch")
        elif self.normalizations is None:
            pass
        elif len(other.normalizations) != len(self.normalizations):
            diff_list.append("len(" + name + "normalizations)")
        else:
            for key in self.normalizations:
                diff_list.extend(
                    self.normalizations[key].compare(
                        other.normalizations[key], name=name + ".normalizations"
                    )
                )
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object
        S += getsizeof(self.symbol)
        S += getsizeof(self.name)
        S += getsizeof(self.unit)
        if self.normalizations is not None:
            for key, value in self.normalizations.items():
                S += getsizeof(value) + getsizeof(key)
        return S

    def as_dict(self, type_handle_ndarray=0, keep_function=False, **kwargs):
        """
        Convert this object in a json serializable dict (can be use in __init__).
        type_handle_ndarray: int
            How to handle ndarray (0: tolist, 1: copy, 2: nothing)
        keep_function : bool
            True to keep the function object, else return str
        Optional keyword input parameter is for internal use only
        and may prevent json serializability.
        """

        Data_dict = dict()
        Data_dict["symbol"] = self.symbol
        Data_dict["name"] = self.name
        Data_dict["unit"] = self.unit
        if self.normalizations is None:
            Data_dict["normalizations"] = None
        else:
            Data_dict["normalizations"] = dict()
            for key, obj in self.normalizations.items():
                if obj is not None:
                    Data_dict["normalizations"][key] = obj.as_dict(
                        type_handle_ndarray=type_handle_ndarray,
                        keep_function=keep_function,
                        **kwargs
                    )
                else:
                    Data_dict["normalizations"][key] = None
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
        if self._normalizations is not None:
            for key, obj in self._normalizations.items():
                if obj is not None:
                    obj.parent = self
        return self._normalizations

    normalizations = property(
        fget=_get_normalizations,
        fset=_set_normalizations,
        doc=u"""Normalizations available for the field and its axes

        :Type: {Normalization}
        """,
    )
