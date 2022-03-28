# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Norm_indices.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//Norm_indices
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
    from ..Methods.Norm_indices.normalize import normalize
except ImportError as error:
    normalize = error


from ._check import InitUnKnowClassError


class Norm_indices(Normalization):
    """Return indices instead of axis values"""

    VERSION = 1

    # cf Methods.Norm_indices.normalize
    if isinstance(normalize, ImportError):
        normalize = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Norm_indices method normalize: " + str(normalize)
                )
            )
        )
    else:
        normalize = normalize
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(self, unit="SI", init_dict=None, init_str=None):
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
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
        # Set the properties (value check and convertion are done in setter)
        # Call Normalization init
        super(Norm_indices, self).__init__(unit=unit)
        # The class is frozen (in Normalization init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        Norm_indices_str = ""
        # Get the properties inherited from Normalization
        Norm_indices_str += super(Norm_indices, self).__str__()
        return Norm_indices_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Normalization
        if not super(Norm_indices, self).__eq__(other):
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
        diff_list.extend(super(Norm_indices, self).compare(other, name=name))
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Normalization
        S += super(Norm_indices, self).__sizeof__()
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
        Norm_indices_dict = super(Norm_indices, self).as_dict(
            type_handle_ndarray=type_handle_ndarray,
            keep_function=keep_function,
            **kwargs
        )
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        Norm_indices_dict["__class__"] = "Norm_indices"
        return Norm_indices_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        # Set to None the properties inherited from Normalization
        super(Norm_indices, self)._set_None()
