# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/DataDual.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//DataDual
"""

from os import linesep
from sys import getsizeof
from ._check import set_array, check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .DataND import DataND

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.DataDual.get_along import get_along
except ImportError as error:
    get_along = error

try:
    from ..Methods.DataDual.get_axes import get_axes
except ImportError as error:
    get_axes = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


class DataDual(DataND):
    """Class for fields defined in both time and freq domains"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.DataDual.get_along
    if isinstance(get_along, ImportError):
        get_along = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataDual method get_along: " + str(get_along))
            )
        )
    else:
        get_along = get_along
    # cf Methods.DataDual.get_axes
    if isinstance(get_axes, ImportError):
        get_axes = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataDual method get_axes: " + str(get_axes))
            )
        )
    else:
        get_axes = get_axes
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self,
        axes_dt=None,
        values_dt=None,
        axes_df=None,
        values_df=None,
        axes=None,
        FTparameters=-1,
        values=None,
        is_real=True,
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
            if "axes_dt" in list(init_dict.keys()):
                axes_dt = init_dict["axes_dt"]
            if "values_dt" in list(init_dict.keys()):
                values_dt = init_dict["values_dt"]
            if "axes_df" in list(init_dict.keys()):
                axes_df = init_dict["axes_df"]
            if "values_df" in list(init_dict.keys()):
                values_df = init_dict["values_df"]
            if "axes" in list(init_dict.keys()):
                axes = init_dict["axes"]
            if "FTparameters" in list(init_dict.keys()):
                FTparameters = init_dict["FTparameters"]
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "is_real" in list(init_dict.keys()):
                is_real = init_dict["is_real"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "normalizations" in list(init_dict.keys()):
                normalizations = init_dict["normalizations"]
        # Set the properties (value check and convertion are done in setter)
        self.axes_dt = axes_dt
        self.values_dt = values_dt
        self.axes_df = axes_df
        self.values_df = values_df
        # Call DataND init
        super(DataDual, self).__init__(
            axes=axes,
            FTparameters=FTparameters,
            values=values,
            is_real=is_real,
            symbol=symbol,
            name=name,
            unit=unit,
            normalizations=normalizations,
        )
        # The class is frozen (in DataND init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        DataDual_str = ""
        # Get the properties inherited from DataND
        DataDual_str += super(DataDual, self).__str__()
        DataDual_str += "axes_dt = " + str(self.axes_dt) + linesep + linesep
        DataDual_str += (
            "values_dt = "
            + linesep
            + str(self.values_dt).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        DataDual_str += "axes_df = " + str(self.axes_df) + linesep + linesep
        DataDual_str += (
            "values_df = "
            + linesep
            + str(self.values_df).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        return DataDual_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from DataND
        if not super(DataDual, self).__eq__(other):
            return False
        if other.axes_dt != self.axes_dt:
            return False
        if not array_equal(other.values_dt, self.values_dt):
            return False
        if other.axes_df != self.axes_df:
            return False
        if not array_equal(other.values_df, self.values_df):
            return False
        return True

    def compare(self, other, name="self", ignore_list=None):
        """Compare two objects and return list of differences"""

        if ignore_list is None:
            ignore_list = list()
        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from DataND
        diff_list.extend(super(DataDual, self).compare(other, name=name))
        if (other.axes_dt is None and self.axes_dt is not None) or (
            other.axes_dt is not None and self.axes_dt is None
        ):
            diff_list.append(name + ".axes_dt None mismatch")
        elif self.axes_dt is None:
            pass
        elif len(other.axes_dt) != len(self.axes_dt):
            diff_list.append("len(" + name + ".axes_dt)")
        else:
            for ii in range(len(other.axes_dt)):
                diff_list.extend(
                    self.axes_dt[ii].compare(
                        other.axes_dt[ii], name=name + ".axes_dt[" + str(ii) + "]"
                    )
                )
        if not array_equal(other.values_dt, self.values_dt):
            diff_list.append(name + ".values_dt")
        if (other.axes_df is None and self.axes_df is not None) or (
            other.axes_df is not None and self.axes_df is None
        ):
            diff_list.append(name + ".axes_df None mismatch")
        elif self.axes_df is None:
            pass
        elif len(other.axes_df) != len(self.axes_df):
            diff_list.append("len(" + name + ".axes_df)")
        else:
            for ii in range(len(other.axes_df)):
                diff_list.extend(
                    self.axes_df[ii].compare(
                        other.axes_df[ii], name=name + ".axes_df[" + str(ii) + "]"
                    )
                )
        if not array_equal(other.values_df, self.values_df):
            diff_list.append(name + ".values_df")
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from DataND
        S += super(DataDual, self).__sizeof__()
        if self.axes_dt is not None:
            for value in self.axes_dt:
                S += getsizeof(value)
        S += getsizeof(self.values_dt)
        if self.axes_df is not None:
            for value in self.axes_df:
                S += getsizeof(value)
        S += getsizeof(self.values_df)
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

        # Get the properties inherited from DataND
        DataDual_dict = super(DataDual, self).as_dict(
            type_handle_ndarray=type_handle_ndarray,
            keep_function=keep_function,
            **kwargs
        )
        if self.axes_dt is None:
            DataDual_dict["axes_dt"] = None
        else:
            DataDual_dict["axes_dt"] = list()
            for obj in self.axes_dt:
                if obj is not None:
                    DataDual_dict["axes_dt"].append(
                        obj.as_dict(
                            type_handle_ndarray=type_handle_ndarray,
                            keep_function=keep_function,
                            **kwargs
                        )
                    )
                else:
                    DataDual_dict["axes_dt"].append(None)
        if self.values_dt is None:
            DataDual_dict["values_dt"] = None
        else:
            if type_handle_ndarray == 0:
                DataDual_dict["values_dt"] = self.values_dt.tolist()
            elif type_handle_ndarray == 1:
                DataDual_dict["values_dt"] = self.values_dt.copy()
            elif type_handle_ndarray == 2:
                DataDual_dict["values_dt"] = self.values_dt
            else:
                raise Exception(
                    "Unknown type_handle_ndarray: " + str(type_handle_ndarray)
                )
        if self.axes_df is None:
            DataDual_dict["axes_df"] = None
        else:
            DataDual_dict["axes_df"] = list()
            for obj in self.axes_df:
                if obj is not None:
                    DataDual_dict["axes_df"].append(
                        obj.as_dict(
                            type_handle_ndarray=type_handle_ndarray,
                            keep_function=keep_function,
                            **kwargs
                        )
                    )
                else:
                    DataDual_dict["axes_df"].append(None)
        if self.values_df is None:
            DataDual_dict["values_df"] = None
        else:
            if type_handle_ndarray == 0:
                DataDual_dict["values_df"] = self.values_df.tolist()
            elif type_handle_ndarray == 1:
                DataDual_dict["values_df"] = self.values_df.copy()
            elif type_handle_ndarray == 2:
                DataDual_dict["values_df"] = self.values_df
            else:
                raise Exception(
                    "Unknown type_handle_ndarray: " + str(type_handle_ndarray)
                )
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        DataDual_dict["__class__"] = "DataDual"
        return DataDual_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.axes_dt = None
        self.values_dt = None
        self.axes_df = None
        self.values_df = None
        # Set to None the properties inherited from DataND
        super(DataDual, self)._set_None()

    def _get_axes_dt(self):
        """getter of axes_dt"""
        if self._axes_dt is not None:
            for obj in self._axes_dt:
                if obj is not None:
                    obj.parent = self
        return self._axes_dt

    def _set_axes_dt(self, value):
        """setter of axes_dt"""
        if type(value) is list:
            for ii, obj in enumerate(value):
                if type(obj) is dict:
                    class_obj = import_class(
                        "SciDataTool.Classes", obj.get("__class__"), "axes_dt"
                    )
                    value[ii] = class_obj(init_dict=obj)
                if value[ii] is not None:
                    value[ii].parent = self
        if value == -1:
            value = list()
        check_var("axes_dt", value, "[Data]")
        self._axes_dt = value

    axes_dt = property(
        fget=_get_axes_dt,
        fset=_set_axes_dt,
        doc=u"""List of the Data1D objects corresponding to the axes in time/space domain

        :Type: [SciDataTool.Classes.Data]
        """,
    )

    def _get_values_dt(self):
        """getter of values_dt"""
        return self._values_dt

    def _set_values_dt(self, value):
        """setter of values_dt"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("values_dt", value, "ndarray")
        self._values_dt = value

    values_dt = property(
        fget=_get_values_dt,
        fset=_set_values_dt,
        doc=u"""Values of the field in time/space domain

        :Type: ndarray
        """,
    )

    def _get_axes_df(self):
        """getter of axes_df"""
        if self._axes_df is not None:
            for obj in self._axes_df:
                if obj is not None:
                    obj.parent = self
        return self._axes_df

    def _set_axes_df(self, value):
        """setter of axes_df"""
        if type(value) is list:
            for ii, obj in enumerate(value):
                if type(obj) is dict:
                    class_obj = import_class(
                        "SciDataTool.Classes", obj.get("__class__"), "axes_df"
                    )
                    value[ii] = class_obj(init_dict=obj)
                if value[ii] is not None:
                    value[ii].parent = self
        if value == -1:
            value = list()
        check_var("axes_df", value, "[Data]")
        self._axes_df = value

    axes_df = property(
        fget=_get_axes_df,
        fset=_set_axes_df,
        doc=u"""List of the Data1D objects corresponding to the axes in fourier domain

        :Type: [SciDataTool.Classes.Data]
        """,
    )

    def _get_values_df(self):
        """getter of values_df"""
        return self._values_df

    def _set_values_df(self, value):
        """setter of values_df"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("values_df", value, "ndarray")
        self._values_df = value

    values_df = property(
        fget=_get_values_df,
        fset=_set_values_df,
        doc=u"""Values of the field in fourier domain

        :Type: ndarray
        """,
    )
