# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Data1D.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//Data1D
"""

from os import linesep
from sys import getsizeof
from ._check import set_array, check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Data import Data

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Data1D.get_values import get_values
except ImportError as error:
    get_values = error

try:
    from ..Methods.Data1D.get_length import get_length
except ImportError as error:
    get_length = error

try:
    from ..Methods.Data1D.get_axis_periodic import get_axis_periodic
except ImportError as error:
    get_axis_periodic = error

try:
    from ..Methods.Data1D.has_period import has_period
except ImportError as error:
    has_period = error

try:
    from ..Methods.Data1D.get_periodicity import get_periodicity
except ImportError as error:
    get_periodicity = error

try:
    from ..Methods.Data1D.to_linspace import to_linspace
except ImportError as error:
    to_linspace = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError
from .Normalization import Normalization


class Data1D(Data):
    """Class for axes defined as vectors"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Data1D.get_values
    if isinstance(get_values, ImportError):
        get_values = property(
            fget=lambda x: raise_(
                ImportError("Can't use Data1D method get_values: " + str(get_values))
            )
        )
    else:
        get_values = get_values
    # cf Methods.Data1D.get_length
    if isinstance(get_length, ImportError):
        get_length = property(
            fget=lambda x: raise_(
                ImportError("Can't use Data1D method get_length: " + str(get_length))
            )
        )
    else:
        get_length = get_length
    # cf Methods.Data1D.get_axis_periodic
    if isinstance(get_axis_periodic, ImportError):
        get_axis_periodic = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Data1D method get_axis_periodic: "
                    + str(get_axis_periodic)
                )
            )
        )
    else:
        get_axis_periodic = get_axis_periodic
    # cf Methods.Data1D.has_period
    if isinstance(has_period, ImportError):
        has_period = property(
            fget=lambda x: raise_(
                ImportError("Can't use Data1D method has_period: " + str(has_period))
            )
        )
    else:
        has_period = has_period
    # cf Methods.Data1D.get_periodicity
    if isinstance(get_periodicity, ImportError):
        get_periodicity = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Data1D method get_periodicity: " + str(get_periodicity)
                )
            )
        )
    else:
        get_periodicity = get_periodicity
    # cf Methods.Data1D.to_linspace
    if isinstance(to_linspace, ImportError):
        to_linspace = property(
            fget=lambda x: raise_(
                ImportError("Can't use Data1D method to_linspace: " + str(to_linspace))
            )
        )
    else:
        to_linspace = to_linspace
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self,
        values=None,
        is_components=False,
        symmetries=-1,
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
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "is_components" in list(init_dict.keys()):
                is_components = init_dict["is_components"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "normalizations" in list(init_dict.keys()):
                normalizations = init_dict["normalizations"]
        # Set the properties (value check and convertion are done in setter)
        self.values = values
        self.is_components = is_components
        self.symmetries = symmetries
        # Call Data init
        super(Data1D, self).__init__(
            symbol=symbol, name=name, unit=unit, normalizations=normalizations
        )
        # The class is frozen (in Data init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        Data1D_str = ""
        # Get the properties inherited from Data
        Data1D_str += super(Data1D, self).__str__()
        Data1D_str += (
            "values = "
            + linesep
            + str(self.values).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        Data1D_str += "is_components = " + str(self.is_components) + linesep
        Data1D_str += "symmetries = " + str(self.symmetries) + linesep
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
        if other.is_components != self.is_components:
            return False
        if other.symmetries != self.symmetries:
            return False
        return True

    def compare(self, other, name="self", ignore_list=None):
        """Compare two objects and return list of differences"""

        if ignore_list is None:
            ignore_list = list()
        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from Data
        diff_list.extend(super(Data1D, self).compare(other, name=name))
        if not array_equal(other.values, self.values):
            diff_list.append(name + ".values")
        if other._is_components != self._is_components:
            diff_list.append(name + ".is_components")
        if other._symmetries != self._symmetries:
            diff_list.append(name + ".symmetries")
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Data
        S += super(Data1D, self).__sizeof__()
        S += getsizeof(self.values)
        S += getsizeof(self.is_components)
        if self.symmetries is not None:
            for key, value in self.symmetries.items():
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

        # Get the properties inherited from Data
        Data1D_dict = super(Data1D, self).as_dict(
            type_handle_ndarray=type_handle_ndarray,
            keep_function=keep_function,
            **kwargs
        )
        if self.values is None:
            Data1D_dict["values"] = None
        else:
            if type_handle_ndarray == 0:
                Data1D_dict["values"] = self.values.tolist()
            elif type_handle_ndarray == 1:
                Data1D_dict["values"] = self.values.copy()
            elif type_handle_ndarray == 2:
                Data1D_dict["values"] = self.values
            else:
                raise Exception(
                    "Unknown type_handle_ndarray: " + str(type_handle_ndarray)
                )
        Data1D_dict["is_components"] = self.is_components
        Data1D_dict["symmetries"] = (
            self.symmetries.copy() if self.symmetries is not None else None
        )
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        Data1D_dict["__class__"] = "Data1D"
        return Data1D_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.values = None
        self.is_components = None
        self.symmetries = None
        # Set to None the properties inherited from Data
        super(Data1D, self)._set_None()

    def _get_values(self):
        """getter of values"""
        return self._values

    def _set_values(self, value):
        """setter of values"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("values", value, "ndarray")
        self._values = value

    values = property(
        fget=_get_values,
        fset=_set_values,
        doc=u"""List or ndarray of the axis values

        :Type: ndarray
        """,
    )

    def _get_is_components(self):
        """getter of is_components"""
        return self._is_components

    def _set_is_components(self, value):
        """setter of is_components"""
        check_var("is_components", value, "bool")
        self._is_components = value

    is_components = property(
        fget=_get_is_components,
        fset=_set_is_components,
        doc=u"""Boolean indicating if the axis values are strings: True if strings

        :Type: bool
        """,
    )

    def _get_symmetries(self):
        """getter of symmetries"""
        return self._symmetries

    def _set_symmetries(self, value):
        """setter of symmetries"""
        if type(value) is int and value == -1:
            value = dict()
        check_var("symmetries", value, "dict")
        self._symmetries = value

    symmetries = property(
        fget=_get_symmetries,
        fset=_set_symmetries,
        doc=u"""Dictionary of the symmetries along each axis, used to reduce storage

        :Type: dict
        """,
    )
