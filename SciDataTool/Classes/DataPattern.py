# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/DataPattern.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//DataPattern
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
    from ..Methods.DataPattern.get_length import get_length
except ImportError as error:
    get_length = error

try:
    from ..Methods.DataPattern.get_values import get_values
except ImportError as error:
    get_values = error

try:
    from ..Methods.DataPattern.has_period import has_period
except ImportError as error:
    has_period = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


class DataPattern(Data):
    """Class for axes defined as vectors"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.DataPattern.get_length
    if isinstance(get_length, ImportError):
        get_length = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataPattern method get_length: " + str(get_length)
                )
            )
        )
    else:
        get_length = get_length
    # cf Methods.DataPattern.get_values
    if isinstance(get_values, ImportError):
        get_values = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataPattern method get_values: " + str(get_values)
                )
            )
        )
    else:
        get_values = get_values
    # cf Methods.DataPattern.has_period
    if isinstance(has_period, ImportError):
        has_period = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataPattern method has_period: " + str(has_period)
                )
            )
        )
    else:
        has_period = has_period
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self,
        rebuild_indices=None,
        unique_indices=None,
        is_step=True,
        values=None,
        is_components=False,
        symmetries=-1,
        values_whole=None,
        is_overlay=False,
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
            if "rebuild_indices" in list(init_dict.keys()):
                rebuild_indices = init_dict["rebuild_indices"]
            if "unique_indices" in list(init_dict.keys()):
                unique_indices = init_dict["unique_indices"]
            if "is_step" in list(init_dict.keys()):
                is_step = init_dict["is_step"]
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "is_components" in list(init_dict.keys()):
                is_components = init_dict["is_components"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
            if "values_whole" in list(init_dict.keys()):
                values_whole = init_dict["values_whole"]
            if "is_overlay" in list(init_dict.keys()):
                is_overlay = init_dict["is_overlay"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "normalizations" in list(init_dict.keys()):
                normalizations = init_dict["normalizations"]
        # Set the properties (value check and convertion are done in setter)
        self.rebuild_indices = rebuild_indices
        self.unique_indices = unique_indices
        self.is_step = is_step
        self.values = values
        self.is_components = is_components
        self.symmetries = symmetries
        self.values_whole = values_whole
        self.is_overlay = is_overlay
        # Call Data init
        super(DataPattern, self).__init__(
            symbol=symbol, name=name, unit=unit, normalizations=normalizations
        )
        # The class is frozen (in Data init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        DataPattern_str = ""
        # Get the properties inherited from Data
        DataPattern_str += super(DataPattern, self).__str__()
        DataPattern_str += (
            "rebuild_indices = "
            + linesep
            + str(self.rebuild_indices).replace(linesep, linesep + "\t")
            + linesep
        )
        DataPattern_str += (
            "unique_indices = "
            + linesep
            + str(self.unique_indices).replace(linesep, linesep + "\t")
            + linesep
        )
        DataPattern_str += "is_step = " + str(self.is_step) + linesep
        DataPattern_str += (
            "values = "
            + linesep
            + str(self.values).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        DataPattern_str += "is_components = " + str(self.is_components) + linesep
        DataPattern_str += "symmetries = " + str(self.symmetries) + linesep
        DataPattern_str += (
            "values_whole = "
            + linesep
            + str(self.values_whole).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        DataPattern_str += "is_overlay = " + str(self.is_overlay) + linesep
        return DataPattern_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Data
        if not super(DataPattern, self).__eq__(other):
            return False
        if other.rebuild_indices != self.rebuild_indices:
            return False
        if other.unique_indices != self.unique_indices:
            return False
        if other.is_step != self.is_step:
            return False
        if not array_equal(other.values, self.values):
            return False
        if other.is_components != self.is_components:
            return False
        if other.symmetries != self.symmetries:
            return False
        if not array_equal(other.values_whole, self.values_whole):
            return False
        if other.is_overlay != self.is_overlay:
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
        diff_list.extend(super(DataPattern, self).compare(other, name=name))
        if other._rebuild_indices != self._rebuild_indices:
            diff_list.append(name + ".rebuild_indices")
        if other._unique_indices != self._unique_indices:
            diff_list.append(name + ".unique_indices")
        if other._is_step != self._is_step:
            diff_list.append(name + ".is_step")
        if not array_equal(other.values, self.values):
            diff_list.append(name + ".values")
        if other._is_components != self._is_components:
            diff_list.append(name + ".is_components")
        if other._symmetries != self._symmetries:
            diff_list.append(name + ".symmetries")
        if not array_equal(other.values_whole, self.values_whole):
            diff_list.append(name + ".values_whole")
        if other._is_overlay != self._is_overlay:
            diff_list.append(name + ".is_overlay")
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Data
        S += super(DataPattern, self).__sizeof__()
        if self.rebuild_indices is not None:
            for value in self.rebuild_indices:
                S += getsizeof(value)
        if self.unique_indices is not None:
            for value in self.unique_indices:
                S += getsizeof(value)
        S += getsizeof(self.is_step)
        S += getsizeof(self.values)
        S += getsizeof(self.is_components)
        if self.symmetries is not None:
            for key, value in self.symmetries.items():
                S += getsizeof(value) + getsizeof(key)
        S += getsizeof(self.values_whole)
        S += getsizeof(self.is_overlay)
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
        DataPattern_dict = super(DataPattern, self).as_dict(
            type_handle_ndarray=type_handle_ndarray,
            keep_function=keep_function,
            **kwargs
        )
        DataPattern_dict["rebuild_indices"] = (
            self.rebuild_indices.copy() if self.rebuild_indices is not None else None
        )
        DataPattern_dict["unique_indices"] = (
            self.unique_indices.copy() if self.unique_indices is not None else None
        )
        DataPattern_dict["is_step"] = self.is_step
        if self.values is None:
            DataPattern_dict["values"] = None
        else:
            if type_handle_ndarray == 0:
                DataPattern_dict["values"] = self.values.tolist()
            elif type_handle_ndarray == 1:
                DataPattern_dict["values"] = self.values.copy()
            elif type_handle_ndarray == 2:
                DataPattern_dict["values"] = self.values
            else:
                raise Exception(
                    "Unknown type_handle_ndarray: " + str(type_handle_ndarray)
                )
        DataPattern_dict["is_components"] = self.is_components
        DataPattern_dict["symmetries"] = (
            self.symmetries.copy() if self.symmetries is not None else None
        )
        if self.values_whole is None:
            DataPattern_dict["values_whole"] = None
        else:
            if type_handle_ndarray == 0:
                DataPattern_dict["values_whole"] = self.values_whole.tolist()
            elif type_handle_ndarray == 1:
                DataPattern_dict["values_whole"] = self.values_whole.copy()
            elif type_handle_ndarray == 2:
                DataPattern_dict["values_whole"] = self.values_whole
            else:
                raise Exception(
                    "Unknown type_handle_ndarray: " + str(type_handle_ndarray)
                )
        DataPattern_dict["is_overlay"] = self.is_overlay
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        DataPattern_dict["__class__"] = "DataPattern"
        return DataPattern_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.rebuild_indices = None
        self.unique_indices = None
        self.is_step = None
        self.values = None
        self.is_components = None
        self.symmetries = None
        self.values_whole = None
        self.is_overlay = None
        # Set to None the properties inherited from Data
        super(DataPattern, self)._set_None()

    def _get_rebuild_indices(self):
        """getter of rebuild_indices"""
        return self._rebuild_indices

    def _set_rebuild_indices(self, value):
        """setter of rebuild_indices"""
        if type(value) is int and value == -1:
            value = list()
        check_var("rebuild_indices", value, "list")
        self._rebuild_indices = value

    rebuild_indices = property(
        fget=_get_rebuild_indices,
        fset=_set_rebuild_indices,
        doc=u"""Indices to rebuild complete axis

        :Type: list
        """,
    )

    def _get_unique_indices(self):
        """getter of unique_indices"""
        return self._unique_indices

    def _set_unique_indices(self, value):
        """setter of unique_indices"""
        if type(value) is int and value == -1:
            value = list()
        check_var("unique_indices", value, "list")
        self._unique_indices = value

    unique_indices = property(
        fget=_get_unique_indices,
        fset=_set_unique_indices,
        doc=u"""Indices which were taken from complete axis

        :Type: list
        """,
    )

    def _get_is_step(self):
        """getter of is_step"""
        return self._is_step

    def _set_is_step(self, value):
        """setter of is_step"""
        check_var("is_step", value, "bool")
        self._is_step = value

    is_step = property(
        fget=_get_is_step,
        fset=_set_is_step,
        doc=u"""True if the axis is defined by step

        :Type: bool
        """,
    )

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
        doc=u"""True if the axis values are strings

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

    def _get_values_whole(self):
        """getter of values_whole"""
        return self._values_whole

    def _set_values_whole(self, value):
        """setter of values_whole"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("values_whole", value, "ndarray")
        self._values_whole = value

    values_whole = property(
        fget=_get_values_whole,
        fset=_set_values_whole,
        doc=u"""Complete axis

        :Type: ndarray
        """,
    )

    def _get_is_overlay(self):
        """getter of is_overlay"""
        return self._is_overlay

    def _set_is_overlay(self, value):
        """setter of is_overlay"""
        check_var("is_overlay", value, "bool")
        self._is_overlay = value

    is_overlay = property(
        fget=_get_is_overlay,
        fset=_set_is_overlay,
        doc=u"""True if axis must be used to overlay curves in plots

        :Type: bool
        """,
    )
