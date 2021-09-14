# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/DataND.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//DataND
"""

from os import linesep
from sys import getsizeof
from logging import getLogger
from ._check import set_array, check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Data import Data

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.DataND._set_values import _set_values
except ImportError as error:
    _set_values = error

try:
    from ..Methods.DataND.comp_axes import comp_axes
except ImportError as error:
    comp_axes = error

try:
    from ..Methods.DataND.compare_along import compare_along
except ImportError as error:
    compare_along = error

try:
    from ..Methods.DataND.compare_magnitude_along import compare_magnitude_along
except ImportError as error:
    compare_magnitude_along = error

try:
    from ..Methods.DataND.compare_phase_along import compare_phase_along
except ImportError as error:
    compare_phase_along = error

try:
    from ..Methods.DataND.compress import compress
except ImportError as error:
    compress = error

try:
    from ..Methods.DataND.convert import convert
except ImportError as error:
    convert = error

try:
    from ..Methods.DataND.export_along import export_along
except ImportError as error:
    export_along = error

try:
    from ..Methods.DataND.extract_slices import extract_slices
except ImportError as error:
    extract_slices = error

try:
    from ..Methods.DataND.extract_slices_fft import extract_slices_fft
except ImportError as error:
    extract_slices_fft = error

try:
    from ..Methods.DataND.get_along import get_along
except ImportError as error:
    get_along = error

try:
    from ..Methods.DataND.get_axes import get_axes
except ImportError as error:
    get_axes = error

try:
    from ..Methods.DataND.get_data_along import get_data_along
except ImportError as error:
    get_data_along = error

try:
    from ..Methods.DataND.get_field import get_field
except ImportError as error:
    get_field = error

try:
    from ..Methods.DataND.get_harmonics import get_harmonics
except ImportError as error:
    get_harmonics = error

try:
    from ..Methods.DataND.get_magnitude_along import get_magnitude_along
except ImportError as error:
    get_magnitude_along = error

try:
    from ..Methods.DataND.get_phase_along import get_phase_along
except ImportError as error:
    get_phase_along = error

try:
    from ..Methods.DataND.has_period import has_period
except ImportError as error:
    has_period = error

try:
    from ..Methods.DataND.interpolate import interpolate
except ImportError as error:
    interpolate = error

try:
    from ..Methods.DataND.plot_2D_Data import plot_2D_Data
except ImportError as error:
    plot_2D_Data = error

try:
    from ..Methods.DataND.plot_2D_Data_Animated import plot_2D_Data_Animated
except ImportError as error:
    plot_2D_Data_Animated = error

try:
    from ..Methods.DataND.plot_3D_Data import plot_3D_Data
except ImportError as error:
    plot_3D_Data = error

try:
    from ..Methods.DataND.rebuild_symmetries import rebuild_symmetries
except ImportError as error:
    rebuild_symmetries = error

try:
    from ..Methods.DataND.set_Ftparameters import set_Ftparameters
except ImportError as error:
    set_Ftparameters = error

try:
    from ..Methods.DataND.orthogonal_mp import orthogonal_mp
except ImportError as error:
    orthogonal_mp = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


class DataND(Data):
    """Abstract class for fields (time or frequency domain)"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.DataND._set_values
    if isinstance(_set_values, ImportError):
        _set_values = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method _set_values: " + str(_set_values))
            )
        )
    else:
        _set_values = _set_values
    # cf Methods.DataND.comp_axes
    if isinstance(comp_axes, ImportError):
        comp_axes = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method comp_axes: " + str(comp_axes))
            )
        )
    else:
        comp_axes = comp_axes
    # cf Methods.DataND.compare_along
    if isinstance(compare_along, ImportError):
        compare_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method compare_along: " + str(compare_along)
                )
            )
        )
    else:
        compare_along = compare_along
    # cf Methods.DataND.compare_magnitude_along
    if isinstance(compare_magnitude_along, ImportError):
        compare_magnitude_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method compare_magnitude_along: "
                    + str(compare_magnitude_along)
                )
            )
        )
    else:
        compare_magnitude_along = compare_magnitude_along
    # cf Methods.DataND.compare_phase_along
    if isinstance(compare_phase_along, ImportError):
        compare_phase_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method compare_phase_along: "
                    + str(compare_phase_along)
                )
            )
        )
    else:
        compare_phase_along = compare_phase_along
    # cf Methods.DataND.compress
    if isinstance(compress, ImportError):
        compress = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method compress: " + str(compress))
            )
        )
    else:
        compress = compress
    # cf Methods.DataND.convert
    if isinstance(convert, ImportError):
        convert = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method convert: " + str(convert))
            )
        )
    else:
        convert = convert
    # cf Methods.DataND.export_along
    if isinstance(export_along, ImportError):
        export_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method export_along: " + str(export_along)
                )
            )
        )
    else:
        export_along = export_along
    # cf Methods.DataND.extract_slices
    if isinstance(extract_slices, ImportError):
        extract_slices = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method extract_slices: " + str(extract_slices)
                )
            )
        )
    else:
        extract_slices = extract_slices
    # cf Methods.DataND.extract_slices_fft
    if isinstance(extract_slices_fft, ImportError):
        extract_slices_fft = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method extract_slices_fft: "
                    + str(extract_slices_fft)
                )
            )
        )
    else:
        extract_slices_fft = extract_slices_fft
    # cf Methods.DataND.get_along
    if isinstance(get_along, ImportError):
        get_along = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method get_along: " + str(get_along))
            )
        )
    else:
        get_along = get_along
    # cf Methods.DataND.get_axes
    if isinstance(get_axes, ImportError):
        get_axes = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method get_axes: " + str(get_axes))
            )
        )
    else:
        get_axes = get_axes
    # cf Methods.DataND.get_data_along
    if isinstance(get_data_along, ImportError):
        get_data_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method get_data_along: " + str(get_data_along)
                )
            )
        )
    else:
        get_data_along = get_data_along
    # cf Methods.DataND.get_field
    if isinstance(get_field, ImportError):
        get_field = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method get_field: " + str(get_field))
            )
        )
    else:
        get_field = get_field
    # cf Methods.DataND.get_harmonics
    if isinstance(get_harmonics, ImportError):
        get_harmonics = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method get_harmonics: " + str(get_harmonics)
                )
            )
        )
    else:
        get_harmonics = get_harmonics
    # cf Methods.DataND.get_magnitude_along
    if isinstance(get_magnitude_along, ImportError):
        get_magnitude_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method get_magnitude_along: "
                    + str(get_magnitude_along)
                )
            )
        )
    else:
        get_magnitude_along = get_magnitude_along
    # cf Methods.DataND.get_phase_along
    if isinstance(get_phase_along, ImportError):
        get_phase_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method get_phase_along: " + str(get_phase_along)
                )
            )
        )
    else:
        get_phase_along = get_phase_along
    # cf Methods.DataND.has_period
    if isinstance(has_period, ImportError):
        has_period = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method has_period: " + str(has_period))
            )
        )
    else:
        has_period = has_period
    # cf Methods.DataND.interpolate
    if isinstance(interpolate, ImportError):
        interpolate = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method interpolate: " + str(interpolate))
            )
        )
    else:
        interpolate = interpolate
    # cf Methods.DataND.plot_2D_Data
    if isinstance(plot_2D_Data, ImportError):
        plot_2D_Data = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method plot_2D_Data: " + str(plot_2D_Data)
                )
            )
        )
    else:
        plot_2D_Data = plot_2D_Data
    # cf Methods.DataND.plot_2D_Data_Animated
    if isinstance(plot_2D_Data_Animated, ImportError):
        plot_2D_Data_Animated = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method plot_2D_Data_Animated: "
                    + str(plot_2D_Data_Animated)
                )
            )
        )
    else:
        plot_2D_Data_Animated = plot_2D_Data_Animated
    # cf Methods.DataND.plot_3D_Data
    if isinstance(plot_3D_Data, ImportError):
        plot_3D_Data = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method plot_3D_Data: " + str(plot_3D_Data)
                )
            )
        )
    else:
        plot_3D_Data = plot_3D_Data
    # cf Methods.DataND.rebuild_symmetries
    if isinstance(rebuild_symmetries, ImportError):
        rebuild_symmetries = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method rebuild_symmetries: "
                    + str(rebuild_symmetries)
                )
            )
        )
    else:
        rebuild_symmetries = rebuild_symmetries
    # cf Methods.DataND.set_Ftparameters
    if isinstance(set_Ftparameters, ImportError):
        set_Ftparameters = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method set_Ftparameters: " + str(set_Ftparameters)
                )
            )
        )
    else:
        set_Ftparameters = set_Ftparameters
    # cf Methods.DataND.orthogonal_mp
    if isinstance(orthogonal_mp, ImportError):
        orthogonal_mp = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataND method orthogonal_mp: " + str(orthogonal_mp)
                )
            )
        )
    else:
        orthogonal_mp = orthogonal_mp
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(self, axes=None, FTparameters=-1, values=None, is_real=True, symbol="", name="", unit="", normalizations=-1, init_dict = None, init_str = None):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for pyleecan type, -1 will call the default constructor
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
        self.axes = axes
        self.FTparameters = FTparameters
        self.values = values
        self.is_real = is_real
        # Call Data init
        super(DataND, self).__init__(symbol=symbol, name=name, unit=unit, normalizations=normalizations)
        # The class is frozen (in Data init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        DataND_str = ""
        # Get the properties inherited from Data
        DataND_str += super(DataND, self).__str__()
        DataND_str += "axes = "+ str(self.axes) + linesep + linesep
        DataND_str += "FTparameters = " + str(self.FTparameters) + linesep
        DataND_str += "values = " + linesep + str(self.values).replace(linesep, linesep + "\t") + linesep + linesep
        DataND_str += "is_real = " + str(self.is_real) + linesep
        return DataND_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Data
        if not super(DataND, self).__eq__(other):
            return False
        if other.axes != self.axes:
            return False
        if other.FTparameters != self.FTparameters:
            return False
        if not array_equal(other.values, self.values):
            return False
        if other.is_real != self.is_real:
            return False
        return True

    def compare(self, other, name='self', ignore_list=None):
        """Compare two objects and return list of differences"""

        if ignore_list is None:
            ignore_list = list()
        if type(other) != type(self):
            return ['type('+name+')']
        diff_list = list()

        # Check the properties inherited from Data
        diff_list.extend(super(DataND, self).compare(other,name=name))
        if (other.axes is None and self.axes is not None) or (other.axes is not None and self.axes is None):
            diff_list.append(name+'.axes None mismatch')
        elif self.axes is None:
            pass
        elif len(other.axes) != len(self.axes):
            diff_list.append('len('+name+'.axes)')
        else:
            for ii in range(len(other.axes)):
                diff_list.extend(self.axes[ii].compare(other.axes[ii],name=name+'.axes['+str(ii)+']'))
        if other._FTparameters != self._FTparameters:
            diff_list.append(name+'.FTparameters')
        if not array_equal(other.values, self.values):
            diff_list.append(name+'.values')
        if other._is_real != self._is_real:
            diff_list.append(name+'.is_real')
        # Filter ignore differences
        diff_list = list(filter(lambda x : x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Data
        S += super(DataND, self).__sizeof__()
        if self.axes is not None:
            for value in self.axes:
                S += getsizeof(value)
        if self.FTparameters is not None:
            for key, value in self.FTparameters.items():
                S += getsizeof(value) + getsizeof(key)
        S += getsizeof(self.values)
        S += getsizeof(self.is_real)
        return S

    def as_dict(self, **kwargs):
        """
        Convert this object in a json serializable dict (can be use in __init__).
        Optional keyword input parameter is for internal use only 
        and may prevent json serializability.
        """

        # Get the properties inherited from Data
        DataND_dict = super(DataND, self).as_dict(**kwargs)
        if self.axes is None:
            DataND_dict["axes"] = None
        else:
            DataND_dict["axes"] = list()
            for obj in self.axes:
                if obj is not None:
                    DataND_dict["axes"].append(obj.as_dict())
                else:
                    DataND_dict["axes"].append(None)
        DataND_dict["FTparameters"] = (
            self.FTparameters.copy() if self.FTparameters is not None else None
        )
        if self.values is None:
            DataND_dict["values"] = None
        else:
            DataND_dict["values"] = self.values.tolist()
        DataND_dict["is_real"] = self.is_real
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        DataND_dict["__class__"] = "DataND"
        return DataND_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.axes = None
        self.FTparameters = None
        self.values = None
        self.is_real = None
        # Set to None the properties inherited from Data
        super(DataND, self)._set_None()

    def _get_axes(self):
        """getter of axes"""
        if self._axes is not None:
            for obj in self._axes:
                if obj is not None:
                    obj.parent = self
        return self._axes

    def _set_axes(self, value):
        """setter of axes"""
        if type(value) is list:
            for ii, obj in enumerate(value):
                if type(obj) is dict:
                    class_obj = import_class('SciDataTool.Classes', obj.get('__class__'), 'axes')
                    value[ii] = class_obj(init_dict=obj)
                if value[ii] is not None:
                    value[ii].parent = self
        if value == -1:
            value = list()
        check_var("axes", value, "[Data]")
        self._axes = value

    axes = property(
        fget=_get_axes,
        fset=_set_axes,
        doc=u"""List of the Data1D objects corresponding to the axes

        :Type: [SciDataTool.Classes.Data]
        """,
    )

    def _get_FTparameters(self):
        """getter of FTparameters"""
        return self._FTparameters

    def _set_FTparameters(self, value):
        """setter of FTparameters"""
        if type(value) is int and value == -1:
            value = dict()
        check_var("FTparameters", value, "dict")
        self._FTparameters = value

    FTparameters = property(
        fget=_get_FTparameters,
        fset=_set_FTparameters,
        doc=u"""Tunable parameters for the Fourier Transforms

        :Type: dict
        """,
    )

    def _get_values(self):
        """getter of values"""
        return self._values

    values = property(
        fget=_get_values,
        fset=_set_values,
        doc=u"""Values of the field

        :Type: ndarray
        """,
    )

    def _get_is_real(self):
        """getter of is_real"""
        return self._is_real

    def _set_is_real(self, value):
        """setter of is_real"""
        check_var("is_real", value, "bool")
        self._is_real = value

    is_real = property(
        fget=_get_is_real,
        fset=_set_is_real,
        doc=u"""To indicate if the signal is real (use only positive frequencies)

        :Type: bool
        """,
    )
