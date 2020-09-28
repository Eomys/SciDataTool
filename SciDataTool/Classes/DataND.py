# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Data/DataND.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//DataND
"""

from os import linesep
from ._check import set_array, check_var, raise_
from ..Functions.save import save
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Data import Data

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
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
    from ..Methods.DataND.set_Ftparameters import set_Ftparameters
except ImportError as error:
    set_Ftparameters = error

try:
    from ..Methods.DataND.comp_axes import comp_axes
except ImportError as error:
    comp_axes = error

try:
    from ..Methods.DataND.convert import convert
except ImportError as error:
    convert = error

try:
    from ..Methods.DataND.extract_slices import extract_slices
except ImportError as error:
    extract_slices = error

try:
    from ..Methods.DataND.extract_slices_fft import extract_slices_fft
except ImportError as error:
    extract_slices_fft = error

try:
    from ..Methods.DataND.get_field import get_field
except ImportError as error:
    get_field = error

try:
    from ..Methods.DataND.rebuild_symmetries import rebuild_symmetries
except ImportError as error:
    rebuild_symmetries = error

try:
    from ..Methods.DataND.interpolate import interpolate
except ImportError as error:
    interpolate = error

try:
    from ..Methods.DataND.get_along import get_along
except ImportError as error:
    get_along = error

try:
    from ..Methods.DataND.get_magnitude_along import get_magnitude_along
except ImportError as error:
    get_magnitude_along = error

try:
    from ..Methods.DataND.get_phase_along import get_phase_along
except ImportError as error:
    get_phase_along = error

try:
    from ..Methods.DataND.get_harmonics import get_harmonics
except ImportError as error:
    get_harmonics = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


class DataND(Data):
    """Abstract class for fields (time or frequency domain)"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
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
    # cf Methods.DataND.comp_axes
    if isinstance(comp_axes, ImportError):
        comp_axes = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method comp_axes: " + str(comp_axes))
            )
        )
    else:
        comp_axes = comp_axes
    # cf Methods.DataND.convert
    if isinstance(convert, ImportError):
        convert = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method convert: " + str(convert))
            )
        )
    else:
        convert = convert
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
    # cf Methods.DataND.get_field
    if isinstance(get_field, ImportError):
        get_field = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method get_field: " + str(get_field))
            )
        )
    else:
        get_field = get_field
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
    # cf Methods.DataND.interpolate
    if isinstance(interpolate, ImportError):
        interpolate = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method interpolate: " + str(interpolate))
            )
        )
    else:
        interpolate = interpolate
    # cf Methods.DataND.get_along
    if isinstance(get_along, ImportError):
        get_along = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataND method get_along: " + str(get_along))
            )
        )
    else:
        get_along = get_along
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
    # save method is available in all object
    save = save

    # generic copy method
    def copy(self):
        """Return a copy of the class
        """
        return type(self)(init_dict=self.as_dict())

    def __init__(
        self,
        axes=None,
        normalizations=-1,
        FTparameters=-1,
        values=None,
        symbol="",
        name="",
        unit="",
        symmetries=-1,
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
            if "axes" in list(init_dict.keys()):
                axes = init_dict["axes"]
            if "normalizations" in list(init_dict.keys()):
                normalizations = init_dict["normalizations"]
            if "FTparameters" in list(init_dict.keys()):
                FTparameters = init_dict["FTparameters"]
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
        # Set the properties (value check and convertion are done in setter)
        self.axes = axes
        self.normalizations = normalizations
        self.FTparameters = FTparameters
        self.values = values
        # Call Data init
        super(DataND, self).__init__(
            symbol=symbol, name=name, unit=unit, symmetries=symmetries
        )
        # The class is frozen (in Data init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        DataND_str = ""
        # Get the properties inherited from Data
        DataND_str += super(DataND, self).__str__()
        DataND_str += "axes = " + str(self.axes) + linesep + linesep
        DataND_str += "normalizations = " + str(self.normalizations) + linesep
        DataND_str += "FTparameters = " + str(self.FTparameters) + linesep
        DataND_str += (
            "values = "
            + linesep
            + str(self.values).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
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
        if other.normalizations != self.normalizations:
            return False
        if other.FTparameters != self.FTparameters:
            return False
        if not array_equal(other.values, self.values):
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        # Get the properties inherited from Data
        DataND_dict = super(DataND, self).as_dict()
        DataND_dict["axes"] = list()
        for obj in self.axes:
            DataND_dict["axes"].append(obj.as_dict())
        DataND_dict["normalizations"] = self.normalizations
        DataND_dict["FTparameters"] = self.FTparameters
        if self.values is None:
            DataND_dict["values"] = None
        else:
            DataND_dict["values"] = self.values.tolist()
        # The class name is added to the dict fordeserialisation purpose
        # Overwrite the mother class name
        DataND_dict["__class__"] = "DataND"
        return DataND_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        self.axes = None
        self.normalizations = None
        self.FTparameters = None
        self.values = None
        # Set to None the properties inherited from Data
        super(DataND, self)._set_None()

    def _get_axes(self):
        """getter of axes"""
        for obj in self._axes:
            if obj is not None:
                obj.parent = self
        return self._axes

    def _set_axes(self, value):
        """setter of axes"""
        if type(value) is list:
            for ii, obj in enumerate(value):
                if type(obj) is dict:
                    class_obj = import_class(
                        "SciDataTool.Classes." + obj.get("__class__"),
                        obj.get("__class__"),
                        "axes",
                    )
                    value[ii] = class_obj(init_dict=obj)
        if value is -1:
            value = list()
        check_var("axes", value, "[Data]")
        self._axes = value

        for obj in self._axes:
            if obj is not None:
                obj.parent = self

    axes = property(
        fget=_get_axes,
        fset=_set_axes,
        doc=u"""List of the Data1D objects corresponding to the axes

        :Type: [SciDataTool.Classes.Data]
        """,
    )

    def _get_normalizations(self):
        """getter of normalizations"""
        return self._normalizations

    def _set_normalizations(self, value):
        """setter of normalizations"""
        if value is -1:
            value = dict()
        check_var("normalizations", value, "dict")
        self._normalizations = value

    normalizations = property(
        fget=_get_normalizations,
        fset=_set_normalizations,
        doc=u"""Normalizations available for the field and its axes

        :Type: dict
        """,
    )

    def _get_FTparameters(self):
        """getter of FTparameters"""
        return self._FTparameters

    def _set_FTparameters(self, value):
        """setter of FTparameters"""
        if value is -1:
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

    def _set_values(self, value):
        """setter of values"""
        if value is -1:
            value = list()
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
        doc=u"""Values of the field

        :Type: ndarray
        """,
    )
