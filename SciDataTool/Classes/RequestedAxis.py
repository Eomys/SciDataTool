# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/RequestedAxis.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//RequestedAxis
"""

from os import linesep
from ._check import set_array, check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from ._frozen import FrozenClass

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.RequestedAxis.get_axis import get_axis
except ImportError as error:
    get_axis = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


class RequestedAxis(FrozenClass):
    """Class to handle requested axes during get_along methods"""

    VERSION = 1

    # cf Methods.RequestedAxis.get_axis
    if isinstance(get_axis, ImportError):
        get_axis = property(
            fget=lambda x: raise_(
                ImportError("Can't use RequestedAxis method get_axis: " + str(get_axis))
            )
        )
    else:
        get_axis = get_axis
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self,
        name="",
        corr_name="",
        unit="",
        corr_unit="",
        extension="",
        values=None,
        indices=None,
        input_data=None,
        operation=None,
        index=None,
        transform=None,
        is_pattern=False,
        rebuild_indices=None,
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
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "corr_name" in list(init_dict.keys()):
                corr_name = init_dict["corr_name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "corr_unit" in list(init_dict.keys()):
                corr_unit = init_dict["corr_unit"]
            if "extension" in list(init_dict.keys()):
                extension = init_dict["extension"]
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "indices" in list(init_dict.keys()):
                indices = init_dict["indices"]
            if "input_data" in list(init_dict.keys()):
                input_data = init_dict["input_data"]
            if "operation" in list(init_dict.keys()):
                operation = init_dict["operation"]
            if "index" in list(init_dict.keys()):
                index = init_dict["index"]
            if "transform" in list(init_dict.keys()):
                transform = init_dict["transform"]
            if "is_pattern" in list(init_dict.keys()):
                is_pattern = init_dict["is_pattern"]
            if "rebuild_indices" in list(init_dict.keys()):
                rebuild_indices = init_dict["rebuild_indices"]
        # Set the properties (value check and convertion are done in setter)
        self.parent = None
        self.name = name
        self.corr_name = corr_name
        self.unit = unit
        self.corr_unit = corr_unit
        self.extension = extension
        self.values = values
        self.indices = indices
        self.input_data = input_data
        self.operation = operation
        self.index = index
        self.transform = transform
        self.is_pattern = is_pattern
        self.rebuild_indices = rebuild_indices

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        RequestedAxis_str = ""
        if self.parent is None:
            RequestedAxis_str += "parent = None " + linesep
        else:
            RequestedAxis_str += (
                "parent = " + str(type(self.parent)) + " object" + linesep
            )
        RequestedAxis_str += 'name = "' + str(self.name) + '"' + linesep
        RequestedAxis_str += 'corr_name = "' + str(self.corr_name) + '"' + linesep
        RequestedAxis_str += 'unit = "' + str(self.unit) + '"' + linesep
        RequestedAxis_str += 'corr_unit = "' + str(self.corr_unit) + '"' + linesep
        RequestedAxis_str += 'extension = "' + str(self.extension) + '"' + linesep
        RequestedAxis_str += (
            "values = "
            + linesep
            + str(self.values).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        RequestedAxis_str += (
            "indices = "
            + linesep
            + str(self.indices).replace(linesep, linesep + "\t")
            + linesep
        )
        RequestedAxis_str += (
            "input_data = "
            + linesep
            + str(self.input_data).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        RequestedAxis_str += 'operation = "' + str(self.operation) + '"' + linesep
        RequestedAxis_str += "index = " + str(self.index) + linesep
        RequestedAxis_str += 'transform = "' + str(self.transform) + '"' + linesep
        RequestedAxis_str += "is_pattern = " + str(self.is_pattern) + linesep
        RequestedAxis_str += (
            "rebuild_indices = "
            + linesep
            + str(self.rebuild_indices).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        return RequestedAxis_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.name != self.name:
            return False
        if other.corr_name != self.corr_name:
            return False
        if other.unit != self.unit:
            return False
        if other.corr_unit != self.corr_unit:
            return False
        if other.extension != self.extension:
            return False
        if not array_equal(other.values, self.values):
            return False
        if other.indices != self.indices:
            return False
        if not array_equal(other.input_data, self.input_data):
            return False
        if other.operation != self.operation:
            return False
        if other.index != self.index:
            return False
        if other.transform != self.transform:
            return False
        if other.is_pattern != self.is_pattern:
            return False
        if not array_equal(other.rebuild_indices, self.rebuild_indices):
            return False
        return True

    def as_dict(self):
        """Convert this object in a json seriable dict (can be use in __init__)"""

        RequestedAxis_dict = dict()
        RequestedAxis_dict["name"] = self.name
        RequestedAxis_dict["corr_name"] = self.corr_name
        RequestedAxis_dict["unit"] = self.unit
        RequestedAxis_dict["corr_unit"] = self.corr_unit
        RequestedAxis_dict["extension"] = self.extension
        if self.values is None:
            RequestedAxis_dict["values"] = None
        else:
            RequestedAxis_dict["values"] = self.values.tolist()
        RequestedAxis_dict["indices"] = (
            self.indices.copy() if self.indices is not None else None
        )
        if self.input_data is None:
            RequestedAxis_dict["input_data"] = None
        else:
            RequestedAxis_dict["input_data"] = self.input_data.tolist()
        RequestedAxis_dict["operation"] = self.operation
        RequestedAxis_dict["index"] = self.index
        RequestedAxis_dict["transform"] = self.transform
        RequestedAxis_dict["is_pattern"] = self.is_pattern
        if self.rebuild_indices is None:
            RequestedAxis_dict["rebuild_indices"] = None
        else:
            RequestedAxis_dict["rebuild_indices"] = self.rebuild_indices.tolist()
        # The class name is added to the dict for deserialisation purpose
        RequestedAxis_dict["__class__"] = "RequestedAxis"
        return RequestedAxis_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.name = None
        self.corr_name = None
        self.unit = None
        self.corr_unit = None
        self.extension = None
        self.values = None
        self.indices = None
        self.input_data = None
        self.operation = None
        self.index = None
        self.transform = None
        self.is_pattern = None
        self.rebuild_indices = None

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
        doc=u"""Name requested in get_along command

        :Type: str
        """,
    )

    def _get_corr_name(self):
        """getter of corr_name"""
        return self._corr_name

    def _set_corr_name(self, value):
        """setter of corr_name"""
        check_var("corr_name", value, "str")
        self._corr_name = value

    corr_name = property(
        fget=_get_corr_name,
        fset=_set_corr_name,
        doc=u"""Corresponding axis if a transform is required

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
        doc=u"""Unit requested in get_along command

        :Type: str
        """,
    )

    def _get_corr_unit(self):
        """getter of corr_unit"""
        return self._corr_unit

    def _set_corr_unit(self, value):
        """setter of corr_unit"""
        check_var("corr_unit", value, "str")
        self._corr_unit = value

    corr_unit = property(
        fget=_get_corr_unit,
        fset=_set_corr_unit,
        doc=u"""Corresponding unit if a transform is required

        :Type: str
        """,
    )

    def _get_extension(self):
        """getter of extension"""
        return self._extension

    def _set_extension(self, value):
        """setter of extension"""
        check_var("extension", value, "str")
        self._extension = value

    extension = property(
        fget=_get_extension,
        fset=_set_extension,
        doc=u"""Extension of the requested axis (single or interval)

        :Type: str
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
        doc=u"""Values of the axis

        :Type: ndarray
        """,
    )

    def _get_indices(self):
        """getter of indices"""
        return self._indices

    def _set_indices(self, value):
        """setter of indices"""
        if type(value) is int and value == -1:
            value = list()
        check_var("indices", value, "list")
        self._indices = value

    indices = property(
        fget=_get_indices,
        fset=_set_indices,
        doc=u"""Indices of the axis

        :Type: list
        """,
    )

    def _get_input_data(self):
        """getter of input_data"""
        return self._input_data

    def _set_input_data(self, value):
        """setter of input_data"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("input_data", value, "ndarray")
        self._input_data = value

    input_data = property(
        fget=_get_input_data,
        fset=_set_input_data,
        doc=u"""Input data to interpolate on

        :Type: ndarray
        """,
    )

    def _get_operation(self):
        """getter of operation"""
        return self._operation

    def _set_operation(self, value):
        """setter of operation"""
        check_var("operation", value, "str")
        self._operation = value

    operation = property(
        fget=_get_operation,
        fset=_set_operation,
        doc=u"""Operation to perform on the axis (coordinate change, etc)

        :Type: str
        """,
    )

    def _get_index(self):
        """getter of index"""
        return self._index

    def _set_index(self, value):
        """setter of index"""
        check_var("index", value, "int")
        self._index = value

    index = property(
        fget=_get_index,
        fset=_set_index,
        doc=u"""Index of the axis in the axes list

        :Type: int
        """,
    )

    def _get_transform(self):
        """getter of transform"""
        return self._transform

    def _set_transform(self, value):
        """setter of transform"""
        check_var("transform", value, "str")
        self._transform = value

    transform = property(
        fget=_get_transform,
        fset=_set_transform,
        doc=u"""Transform to perform on the axis (fft, ifft)

        :Type: str
        """,
    )

    def _get_is_pattern(self):
        """getter of is_pattern"""
        return self._is_pattern

    def _set_is_pattern(self, value):
        """setter of is_pattern"""
        check_var("is_pattern", value, "bool")
        self._is_pattern = value

    is_pattern = property(
        fget=_get_is_pattern,
        fset=_set_is_pattern,
        doc=u"""To indicate if the axis is a DataPattern

        :Type: bool
        """,
    )

    def _get_rebuild_indices(self):
        """getter of rebuild_indices"""
        return self._rebuild_indices

    def _set_rebuild_indices(self, value):
        """setter of rebuild_indices"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("rebuild_indices", value, "ndarray")
        self._rebuild_indices = value

    rebuild_indices = property(
        fget=_get_rebuild_indices,
        fset=_set_rebuild_indices,
        doc=u"""Indices to rebuild pattern

        :Type: ndarray
        """,
    )
