# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Norm_func.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//Norm_func
"""

from os import linesep
from sys import getsizeof
from ._check import check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Normalization import Normalization

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Norm_func.normalize import normalize
except ImportError as error:
    normalize = error


from ntpath import basename
from os.path import isfile
from ._check import CheckTypeError
import numpy as np
import random
from ._check import InitUnKnowClassError


class Norm_func(Normalization):
    """Function normalization (lambda x: function(axis))"""

    VERSION = 1

    # cf Methods.Norm_func.normalize
    if isinstance(normalize, ImportError):
        normalize = property(
            fget=lambda x: raise_(
                ImportError("Can't use Norm_func method normalize: " + str(normalize))
            )
        )
    else:
        normalize = normalize
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(self, function=None, unit="SI", init_dict=None, init_str=None):
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
            if "function" in list(init_dict.keys()):
                function = init_dict["function"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
        # Set the properties (value check and convertion are done in setter)
        self.function = function
        # Call Normalization init
        super(Norm_func, self).__init__(unit=unit)
        # The class is frozen (in Normalization init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        Norm_func_str = ""
        # Get the properties inherited from Normalization
        Norm_func_str += super(Norm_func, self).__str__()
        if self._function_str is not None:
            Norm_func_str += "function = " + self._function_str + linesep
        elif self._function_func is not None:
            Norm_func_str += "function = " + str(self._function_func) + linesep
        else:
            Norm_func_str += "function = None" + linesep + linesep
        return Norm_func_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Normalization
        if not super(Norm_func, self).__eq__(other):
            return False
        if other._function_str != self._function_str:
            return False
        return True

    def compare(self, other, name="self", ignore_list=None):
        """Compare two objects and return list of differences"""

        if ignore_list is None:
            ignore_list = list()
        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from Normalization
        diff_list.extend(super(Norm_func, self).compare(other, name=name))
        if other._function_str != self._function_str:
            diff_list.append(name + ".function")
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Normalization
        S += super(Norm_func, self).__sizeof__()
        S += getsizeof(self._function_str)
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

        # Get the properties inherited from Normalization
        Norm_func_dict = super(Norm_func, self).as_dict(
            type_handle_ndarray=type_handle_ndarray,
            keep_function=keep_function,
            **kwargs,
        )
        if self._function_str is not None:
            Norm_func_dict["function"] = self._function_str
        elif "keep_function" in kwargs and kwargs["keep_function"]:
            Norm_func_dict["function"] = self.function
        else:
            Norm_func_dict["function"] = None
            if self.function is not None:
                self.get_logger().warning(
                    "Norm_func.as_dict(): "
                    + f"Function {self.function.__name__} is not serializable "
                    + "and will be converted to None."
                )
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        Norm_func_dict["__class__"] = "Norm_func"
        return Norm_func_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.function = None
        # Set to None the properties inherited from Normalization
        super(Norm_func, self)._set_None()

    def _get_function(self):
        """getter of function"""
        return self._function_func

    def _set_function(self, value):
        """setter of function"""
        if value is None:
            self._function_str = None
            self._function_func = None
        elif isinstance(value, str) and "lambda" in value:
            self._function_str = value
            self._function_func = eval(value)
        elif isinstance(value, str) and isfile(value) and value[-3:] == ".py":
            self._function_str = value
            f = open(value, "r")
            exec(f.read(), globals())
            self._function_func = eval(basename(value[:-3]))
        elif callable(value):
            self._function_str = None
            self._function_func = value
        else:
            raise CheckTypeError(
                "For property function Expected function or str (path to python file or lambda), got: "
                + str(type(value))
            )

    function = property(
        fget=_get_function,
        fset=_set_function,
        doc="""function to apply

        :Type: function
        """,
    )
