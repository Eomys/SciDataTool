# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/DataLinspace.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//DataLinspace
"""

from os import linesep
from sys import getsizeof
from ._check import check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Data import Data

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.DataLinspace.get_values import get_values
except ImportError as error:
    get_values = error

try:
    from ..Methods.DataLinspace.get_length import get_length
except ImportError as error:
    get_length = error

try:
    from ..Methods.DataLinspace.get_axis_periodic import get_axis_periodic
except ImportError as error:
    get_axis_periodic = error

try:
    from ..Methods.DataLinspace.has_period import has_period
except ImportError as error:
    has_period = error

try:
    from ..Methods.DataLinspace.get_periodicity import get_periodicity
except ImportError as error:
    get_periodicity = error


from ._check import InitUnKnowClassError


class DataLinspace(Data):
    """Class for axes defined as linspaces"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.DataLinspace.get_values
    if isinstance(get_values, ImportError):
        get_values = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataLinspace method get_values: " + str(get_values)
                )
            )
        )
    else:
        get_values = get_values
    # cf Methods.DataLinspace.get_length
    if isinstance(get_length, ImportError):
        get_length = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataLinspace method get_length: " + str(get_length)
                )
            )
        )
    else:
        get_length = get_length
    # cf Methods.DataLinspace.get_axis_periodic
    if isinstance(get_axis_periodic, ImportError):
        get_axis_periodic = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataLinspace method get_axis_periodic: "
                    + str(get_axis_periodic)
                )
            )
        )
    else:
        get_axis_periodic = get_axis_periodic
    # cf Methods.DataLinspace.has_period
    if isinstance(has_period, ImportError):
        has_period = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataLinspace method has_period: " + str(has_period)
                )
            )
        )
    else:
        has_period = has_period
    # cf Methods.DataLinspace.get_periodicity
    if isinstance(get_periodicity, ImportError):
        get_periodicity = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataLinspace method get_periodicity: "
                    + str(get_periodicity)
                )
            )
        )
    else:
        get_periodicity = get_periodicity
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self,
        initial=None,
        final=None,
        step=None,
        number=None,
        include_endpoint=True,
        is_components=False,
        symmetries=-1,
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
            if "initial" in list(init_dict.keys()):
                initial = init_dict["initial"]
            if "final" in list(init_dict.keys()):
                final = init_dict["final"]
            if "step" in list(init_dict.keys()):
                step = init_dict["step"]
            if "number" in list(init_dict.keys()):
                number = init_dict["number"]
            if "include_endpoint" in list(init_dict.keys()):
                include_endpoint = init_dict["include_endpoint"]
            if "is_components" in list(init_dict.keys()):
                is_components = init_dict["is_components"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
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
        self.initial = initial
        self.final = final
        self.step = step
        self.number = number
        self.include_endpoint = include_endpoint
        self.is_components = is_components
        self.symmetries = symmetries
        self.is_overlay = is_overlay
        # Call Data init
        super(DataLinspace, self).__init__(
            symbol=symbol, name=name, unit=unit, normalizations=normalizations
        )
        # The class is frozen (in Data init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        DataLinspace_str = ""
        # Get the properties inherited from Data
        DataLinspace_str += super(DataLinspace, self).__str__()
        DataLinspace_str += "initial = " + str(self.initial) + linesep
        DataLinspace_str += "final = " + str(self.final) + linesep
        DataLinspace_str += "step = " + str(self.step) + linesep
        DataLinspace_str += "number = " + str(self.number) + linesep
        DataLinspace_str += "include_endpoint = " + str(self.include_endpoint) + linesep
        DataLinspace_str += "is_components = " + str(self.is_components) + linesep
        DataLinspace_str += "symmetries = " + str(self.symmetries) + linesep
        DataLinspace_str += "is_overlay = " + str(self.is_overlay) + linesep
        return DataLinspace_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Data
        if not super(DataLinspace, self).__eq__(other):
            return False
        if other.initial != self.initial:
            return False
        if other.final != self.final:
            return False
        if other.step != self.step:
            return False
        if other.number != self.number:
            return False
        if other.include_endpoint != self.include_endpoint:
            return False
        if other.is_components != self.is_components:
            return False
        if other.symmetries != self.symmetries:
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
        diff_list.extend(super(DataLinspace, self).compare(other, name=name))
        if other._initial != self._initial:
            diff_list.append(name + ".initial")
        if other._final != self._final:
            diff_list.append(name + ".final")
        if other._step != self._step:
            diff_list.append(name + ".step")
        if other._number != self._number:
            diff_list.append(name + ".number")
        if other._include_endpoint != self._include_endpoint:
            diff_list.append(name + ".include_endpoint")
        if other._is_components != self._is_components:
            diff_list.append(name + ".is_components")
        if other._symmetries != self._symmetries:
            diff_list.append(name + ".symmetries")
        if other._is_overlay != self._is_overlay:
            diff_list.append(name + ".is_overlay")
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Data
        S += super(DataLinspace, self).__sizeof__()
        S += getsizeof(self.initial)
        S += getsizeof(self.final)
        S += getsizeof(self.step)
        S += getsizeof(self.number)
        S += getsizeof(self.include_endpoint)
        S += getsizeof(self.is_components)
        if self.symmetries is not None:
            for key, value in self.symmetries.items():
                S += getsizeof(value) + getsizeof(key)
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
        DataLinspace_dict = super(DataLinspace, self).as_dict(
            type_handle_ndarray=type_handle_ndarray,
            keep_function=keep_function,
            **kwargs
        )
        DataLinspace_dict["initial"] = self.initial
        DataLinspace_dict["final"] = self.final
        DataLinspace_dict["step"] = self.step
        DataLinspace_dict["number"] = self.number
        DataLinspace_dict["include_endpoint"] = self.include_endpoint
        DataLinspace_dict["is_components"] = self.is_components
        DataLinspace_dict["symmetries"] = (
            self.symmetries.copy() if self.symmetries is not None else None
        )
        DataLinspace_dict["is_overlay"] = self.is_overlay
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        DataLinspace_dict["__class__"] = "DataLinspace"
        return DataLinspace_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.initial = None
        self.final = None
        self.step = None
        self.number = None
        self.include_endpoint = None
        self.is_components = None
        self.symmetries = None
        self.is_overlay = None
        # Set to None the properties inherited from Data
        super(DataLinspace, self)._set_None()

    def _get_initial(self):
        """getter of initial"""
        return self._initial

    def _set_initial(self, value):
        """setter of initial"""
        check_var("initial", value, "float")
        self._initial = value

    initial = property(
        fget=_get_initial,
        fset=_set_initial,
        doc=u"""First value

        :Type: float
        """,
    )

    def _get_final(self):
        """getter of final"""
        return self._final

    def _set_final(self, value):
        """setter of final"""
        check_var("final", value, "float")
        self._final = value

    final = property(
        fget=_get_final,
        fset=_set_final,
        doc=u"""Last value

        :Type: float
        """,
    )

    def _get_step(self):
        """getter of step"""
        return self._step

    def _set_step(self, value):
        """setter of step"""
        check_var("step", value, "float")
        self._step = value

    step = property(
        fget=_get_step,
        fset=_set_step,
        doc=u"""Step

        :Type: float
        """,
    )

    def _get_number(self):
        """getter of number"""
        return self._number

    def _set_number(self, value):
        """setter of number"""
        check_var("number", value, "int")
        self._number = value

    number = property(
        fget=_get_number,
        fset=_set_number,
        doc=u"""Number of steps

        :Type: int
        """,
    )

    def _get_include_endpoint(self):
        """getter of include_endpoint"""
        return self._include_endpoint

    def _set_include_endpoint(self, value):
        """setter of include_endpoint"""
        check_var("include_endpoint", value, "bool")
        self._include_endpoint = value

    include_endpoint = property(
        fget=_get_include_endpoint,
        fset=_set_include_endpoint,
        doc=u"""True if the endpoint must be included

        :Type: bool
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
