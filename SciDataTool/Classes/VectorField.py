# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/VectorField.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//VectorField
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
    from ..Methods.VectorField.change_periodicity import change_periodicity
except ImportError as error:
    change_periodicity = error

try:
    from ..Methods.VectorField.change_referential import change_referential
except ImportError as error:
    change_referential = error

try:
    from ..Methods.VectorField.filter_spectral_leakage import filter_spectral_leakage
except ImportError as error:
    filter_spectral_leakage = error

try:
    from ..Methods.VectorField.freq_to_time import freq_to_time
except ImportError as error:
    freq_to_time = error

try:
    from ..Methods.VectorField.get_axes import get_axes
except ImportError as error:
    get_axes = error

try:
    from ..Methods.VectorField.get_harm_rphiz_along import get_harm_rphiz_along
except ImportError as error:
    get_harm_rphiz_along = error

try:
    from ..Methods.VectorField.get_harm_xyz_along import get_harm_xyz_along
except ImportError as error:
    get_harm_xyz_along = error

try:
    from ..Methods.VectorField.get_mag_rphiz_along import get_mag_rphiz_along
except ImportError as error:
    get_mag_rphiz_along = error

try:
    from ..Methods.VectorField.get_mag_xyz_along import get_mag_xyz_along
except ImportError as error:
    get_mag_xyz_along = error

try:
    from ..Methods.VectorField.get_rphiz_along import get_rphiz_along
except ImportError as error:
    get_rphiz_along = error

try:
    from ..Methods.VectorField.get_xyz_along import get_xyz_along
except ImportError as error:
    get_xyz_along = error

try:
    from ..Methods.VectorField.get_vectorfield_along import get_vectorfield_along
except ImportError as error:
    get_vectorfield_along = error

try:
    from ..Methods.VectorField.plot import plot
except ImportError as error:
    plot = error

try:
    from ..Methods.VectorField.plot_2D_Data import plot_2D_Data
except ImportError as error:
    plot_2D_Data = error

try:
    from ..Methods.VectorField.plot_2D_Data_Animated import plot_2D_Data_Animated
except ImportError as error:
    plot_2D_Data_Animated = error

try:
    from ..Methods.VectorField.plot_3D_Data import plot_3D_Data
except ImportError as error:
    plot_3D_Data = error

try:
    from ..Methods.VectorField.time_to_freq import time_to_freq
except ImportError as error:
    time_to_freq = error

try:
    from ..Methods.VectorField.to_xyz import to_xyz
except ImportError as error:
    to_xyz = error

try:
    from ..Methods.VectorField.to_rphiz import to_rphiz
except ImportError as error:
    to_rphiz = error


from ._check import InitUnKnowClassError


class VectorField(FrozenClass):
    """Class for 2D or 3D vector fields (time or frequency domain)"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.VectorField.change_periodicity
    if isinstance(change_periodicity, ImportError):
        change_periodicity = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method change_periodicity: "
                    + str(change_periodicity)
                )
            )
        )
    else:
        change_periodicity = change_periodicity
    # cf Methods.VectorField.change_referential
    if isinstance(change_referential, ImportError):
        change_referential = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method change_referential: "
                    + str(change_referential)
                )
            )
        )
    else:
        change_referential = change_referential
    # cf Methods.VectorField.filter_spectral_leakage
    if isinstance(filter_spectral_leakage, ImportError):
        filter_spectral_leakage = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method filter_spectral_leakage: "
                    + str(filter_spectral_leakage)
                )
            )
        )
    else:
        filter_spectral_leakage = filter_spectral_leakage
    # cf Methods.VectorField.freq_to_time
    if isinstance(freq_to_time, ImportError):
        freq_to_time = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method freq_to_time: " + str(freq_to_time)
                )
            )
        )
    else:
        freq_to_time = freq_to_time
    # cf Methods.VectorField.get_axes
    if isinstance(get_axes, ImportError):
        get_axes = property(
            fget=lambda x: raise_(
                ImportError("Can't use VectorField method get_axes: " + str(get_axes))
            )
        )
    else:
        get_axes = get_axes
    # cf Methods.VectorField.get_harm_rphiz_along
    if isinstance(get_harm_rphiz_along, ImportError):
        get_harm_rphiz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_harm_rphiz_along: "
                    + str(get_harm_rphiz_along)
                )
            )
        )
    else:
        get_harm_rphiz_along = get_harm_rphiz_along
    # cf Methods.VectorField.get_harm_xyz_along
    if isinstance(get_harm_xyz_along, ImportError):
        get_harm_xyz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_harm_xyz_along: "
                    + str(get_harm_xyz_along)
                )
            )
        )
    else:
        get_harm_xyz_along = get_harm_xyz_along
    # cf Methods.VectorField.get_mag_rphiz_along
    if isinstance(get_mag_rphiz_along, ImportError):
        get_mag_rphiz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_mag_rphiz_along: "
                    + str(get_mag_rphiz_along)
                )
            )
        )
    else:
        get_mag_rphiz_along = get_mag_rphiz_along
    # cf Methods.VectorField.get_mag_xyz_along
    if isinstance(get_mag_xyz_along, ImportError):
        get_mag_xyz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_mag_xyz_along: "
                    + str(get_mag_xyz_along)
                )
            )
        )
    else:
        get_mag_xyz_along = get_mag_xyz_along
    # cf Methods.VectorField.get_rphiz_along
    if isinstance(get_rphiz_along, ImportError):
        get_rphiz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_rphiz_along: "
                    + str(get_rphiz_along)
                )
            )
        )
    else:
        get_rphiz_along = get_rphiz_along
    # cf Methods.VectorField.get_xyz_along
    if isinstance(get_xyz_along, ImportError):
        get_xyz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_xyz_along: " + str(get_xyz_along)
                )
            )
        )
    else:
        get_xyz_along = get_xyz_along
    # cf Methods.VectorField.get_vectorfield_along
    if isinstance(get_vectorfield_along, ImportError):
        get_vectorfield_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_vectorfield_along: "
                    + str(get_vectorfield_along)
                )
            )
        )
    else:
        get_vectorfield_along = get_vectorfield_along
    # cf Methods.VectorField.plot
    if isinstance(plot, ImportError):
        plot = property(
            fget=lambda x: raise_(
                ImportError("Can't use VectorField method plot: " + str(plot))
            )
        )
    else:
        plot = plot
    # cf Methods.VectorField.plot_2D_Data
    if isinstance(plot_2D_Data, ImportError):
        plot_2D_Data = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method plot_2D_Data: " + str(plot_2D_Data)
                )
            )
        )
    else:
        plot_2D_Data = plot_2D_Data
    # cf Methods.VectorField.plot_2D_Data_Animated
    if isinstance(plot_2D_Data_Animated, ImportError):
        plot_2D_Data_Animated = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method plot_2D_Data_Animated: "
                    + str(plot_2D_Data_Animated)
                )
            )
        )
    else:
        plot_2D_Data_Animated = plot_2D_Data_Animated
    # cf Methods.VectorField.plot_3D_Data
    if isinstance(plot_3D_Data, ImportError):
        plot_3D_Data = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method plot_3D_Data: " + str(plot_3D_Data)
                )
            )
        )
    else:
        plot_3D_Data = plot_3D_Data
    # cf Methods.VectorField.time_to_freq
    if isinstance(time_to_freq, ImportError):
        time_to_freq = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method time_to_freq: " + str(time_to_freq)
                )
            )
        )
    else:
        time_to_freq = time_to_freq
    # cf Methods.VectorField.to_xyz
    if isinstance(to_xyz, ImportError):
        to_xyz = property(
            fget=lambda x: raise_(
                ImportError("Can't use VectorField method to_xyz: " + str(to_xyz))
            )
        )
    else:
        to_xyz = to_xyz
    # cf Methods.VectorField.to_rphiz
    if isinstance(to_rphiz, ImportError):
        to_rphiz = property(
            fget=lambda x: raise_(
                ImportError("Can't use VectorField method to_rphiz: " + str(to_rphiz))
            )
        )
    else:
        to_rphiz = to_rphiz
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self, name="", symbol="", components=-1, init_dict=None, init_str=None
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
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "components" in list(init_dict.keys()):
                components = init_dict["components"]
        # Set the properties (value check and convertion are done in setter)
        self.parent = None
        self.name = name
        self.symbol = symbol
        self.components = components

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        VectorField_str = ""
        if self.parent is None:
            VectorField_str += "parent = None " + linesep
        else:
            VectorField_str += (
                "parent = " + str(type(self.parent)) + " object" + linesep
            )
        VectorField_str += 'name = "' + str(self.name) + '"' + linesep
        VectorField_str += 'symbol = "' + str(self.symbol) + '"' + linesep
        VectorField_str += "components = " + str(self.components) + linesep + linesep
        return VectorField_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.name != self.name:
            return False
        if other.symbol != self.symbol:
            return False
        if other.components != self.components:
            return False
        return True

    def compare(self, other, name="self", ignore_list=None):
        """Compare two objects and return list of differences"""

        if ignore_list is None:
            ignore_list = list()
        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()
        if other._name != self._name:
            diff_list.append(name + ".name")
        if other._symbol != self._symbol:
            diff_list.append(name + ".symbol")
        if (other.components is None and self.components is not None) or (
            other.components is not None and self.components is None
        ):
            diff_list.append(name + ".components None mismatch")
        elif self.components is None:
            pass
        elif len(other.components) != len(self.components):
            diff_list.append("len(" + name + "components)")
        else:
            for key in self.components:
                diff_list.extend(
                    self.components[key].compare(
                        other.components[key], name=name + ".components"
                    )
                )
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object
        S += getsizeof(self.name)
        S += getsizeof(self.symbol)
        if self.components is not None:
            for key, value in self.components.items():
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

        VectorField_dict = dict()
        VectorField_dict["name"] = self.name
        VectorField_dict["symbol"] = self.symbol
        if self.components is None:
            VectorField_dict["components"] = None
        else:
            VectorField_dict["components"] = dict()
            for key, obj in self.components.items():
                if obj is not None:
                    VectorField_dict["components"][key] = obj.as_dict(
                        type_handle_ndarray=type_handle_ndarray,
                        keep_function=keep_function,
                        **kwargs
                    )
                else:
                    VectorField_dict["components"][key] = None
        # The class name is added to the dict for deserialisation purpose
        VectorField_dict["__class__"] = "VectorField"
        return VectorField_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.name = None
        self.symbol = None
        self.components = None

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
        doc=u"""Name of the vector field

        :Type: str
        """,
    )

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
        doc=u"""Symbol of the vector field

        :Type: str
        """,
    )

    def _get_components(self):
        """getter of components"""
        if self._components is not None:
            for key, obj in self._components.items():
                if obj is not None:
                    obj.parent = self
        return self._components

    def _set_components(self, value):
        """setter of components"""
        if type(value) is dict:
            for key, obj in value.items():
                if type(obj) is dict:
                    class_obj = import_class(
                        "SciDataTool.Classes", obj.get("__class__"), "components"
                    )
                    value[key] = class_obj(init_dict=obj)
        if type(value) is int and value == -1:
            value = dict()
        check_var("components", value, "{DataND}")
        self._components = value

    components = property(
        fget=_get_components,
        fset=_set_components,
        doc=u"""Dict of the components

        :Type: {SciDataTool.Classes.DataND}
        """,
    )
