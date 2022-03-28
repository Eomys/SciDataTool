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

try:
    from ..Methods.Data1D.get_filter import get_filter
except ImportError as error:
    get_filter = error

try:
    from ..Methods.Data1D.check_filter import check_filter
except ImportError as error:
    check_filter = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


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
    # cf Methods.Data1D.get_filter
    if isinstance(get_filter, ImportError):
        get_filter = property(
            fget=lambda x: raise_(
                ImportError("Can't use Data1D method get_filter: " + str(get_filter))
            )
        )
    else:
        get_filter = get_filter
    # cf Methods.Data1D.check_filter
    if isinstance(check_filter, ImportError):
        check_filter = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Data1D method check_filter: " + str(check_filter)
                )
            )
        )
    else:
        check_filter = check_filter
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self,
        values=None,
        is_components=False,
        symmetries=-1,
        is_overlay=False,
        delimiter=None,
        sort_indices=None,
        filter=None,
        char_to_rm=None,
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
            if "is_overlay" in list(init_dict.keys()):
                is_overlay = init_dict["is_overlay"]
            if "delimiter" in list(init_dict.keys()):
                delimiter = init_dict["delimiter"]
            if "sort_indices" in list(init_dict.keys()):
                sort_indices = init_dict["sort_indices"]
            if "filter" in list(init_dict.keys()):
                filter = init_dict["filter"]
            if "char_to_rm" in list(init_dict.keys()):
                char_to_rm = init_dict["char_to_rm"]
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
        self.is_overlay = is_overlay
        self.delimiter = delimiter
        self.sort_indices = sort_indices
        self.filter = filter
        self.char_to_rm = char_to_rm
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
        Data1D_str += "is_overlay = " + str(self.is_overlay) + linesep
        Data1D_str += 'delimiter = "' + str(self.delimiter) + '"' + linesep
        Data1D_str += (
            "sort_indices = "
            + linesep
            + str(self.sort_indices).replace(linesep, linesep + "\t")
            + linesep
        )
        Data1D_str += "filter = " + str(self.filter) + linesep
        Data1D_str += (
            "char_to_rm = "
            + linesep
            + str(self.char_to_rm).replace(linesep, linesep + "\t")
            + linesep
        )
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
        if other.is_overlay != self.is_overlay:
            return False
        if other.delimiter != self.delimiter:
            return False
        if other.sort_indices != self.sort_indices:
            return False
        if other.filter != self.filter:
            return False
        if other.char_to_rm != self.char_to_rm:
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
        if other._is_overlay != self._is_overlay:
            diff_list.append(name + ".is_overlay")
        if other._delimiter != self._delimiter:
            diff_list.append(name + ".delimiter")
        if other._sort_indices != self._sort_indices:
            diff_list.append(name + ".sort_indices")
        if other._filter != self._filter:
            diff_list.append(name + ".filter")
        if other._char_to_rm != self._char_to_rm:
            diff_list.append(name + ".char_to_rm")
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
        S += getsizeof(self.is_overlay)
        S += getsizeof(self.delimiter)
        if self.sort_indices is not None:
            for value in self.sort_indices:
                S += getsizeof(value)
        if self.filter is not None:
            for key, value in self.filter.items():
                S += getsizeof(value) + getsizeof(key)
        if self.char_to_rm is not None:
            for value in self.char_to_rm:
                S += getsizeof(value)
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
        Data1D_dict["is_overlay"] = self.is_overlay
        Data1D_dict["delimiter"] = self.delimiter
        Data1D_dict["sort_indices"] = (
            self.sort_indices.copy() if self.sort_indices is not None else None
        )
        Data1D_dict["filter"] = self.filter.copy() if self.filter is not None else None
        Data1D_dict["char_to_rm"] = (
            self.char_to_rm.copy() if self.char_to_rm is not None else None
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
        self.is_overlay = None
        self.delimiter = None
        self.sort_indices = None
        self.filter = None
        self.char_to_rm = None
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

    def _get_delimiter(self):
        """getter of delimiter"""
        return self._delimiter

    def _set_delimiter(self, value):
        """setter of delimiter"""
        check_var("delimiter", value, "str")
        self._delimiter = value

    delimiter = property(
        fget=_get_delimiter,
        fset=_set_delimiter,
        doc=u"""Character used to separate attributes in string case (e.g. "r=0, stator, radial")

        :Type: str
        """,
    )

    def _get_sort_indices(self):
        """getter of sort_indices"""
        return self._sort_indices

    def _set_sort_indices(self, value):
        """setter of sort_indices"""
        if type(value) is int and value == -1:
            value = list()
        check_var("sort_indices", value, "list")
        self._sort_indices = value

    sort_indices = property(
        fget=_get_sort_indices,
        fset=_set_sort_indices,
        doc=u"""List of indices to use to sort axis

        :Type: list
        """,
    )

    def _get_filter(self):
        """getter of filter"""
        return self._filter

    def _set_filter(self, value):
        """setter of filter"""
        if type(value) is int and value == -1:
            value = dict()
        check_var("filter", value, "dict")
        self._filter = value

    filter = property(
        fget=_get_filter,
        fset=_set_filter,
        doc=u"""Dict of filter keys

        :Type: dict
        """,
    )

    def _get_char_to_rm(self):
        """getter of char_to_rm"""
        return self._char_to_rm

    def _set_char_to_rm(self, value):
        """setter of char_to_rm"""
        if type(value) is int and value == -1:
            value = list()
        check_var("char_to_rm", value, "list")
        self._char_to_rm = value

    char_to_rm = property(
        fget=_get_char_to_rm,
        fset=_set_char_to_rm,
        doc=u"""List of characters to remove in filter table

        :Type: list
        """,
    )
