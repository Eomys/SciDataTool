# -*- coding: utf-8 -*-
"""File generated according to SciDataTool/Generator/ClassesRef/Output/DataTime.csv
WARNING! All changes made in this file will be lost!
"""
from os import linesep
from SciDataTool.Classes._check import set_array, check_init_dict, check_var, raise_
from SciDataTool.Functions.save import save
from SciDataTool.Classes.DataND import DataND
# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from SciDataTool.Methods.Output.DataTime.get_axis import get_axis
except ImportError as error:
    get_axis = error
try:
    from SciDataTool.Methods.Output.DataTime.get_FT_axis import get_FT_axis
except ImportError as error:
    get_FT_axis = error
try:
    from SciDataTool.Methods.Output.DataTime.get_along import get_along
except ImportError as error:
    get_along = error
try:
    from SciDataTool.Methods.Output.DataTime.get_FT_along import get_FT_along
except ImportError as error:
    get_FT_along = error
try:
    from SciDataTool.Methods.Output.DataTime.get_magnitude_along import get_magnitude_along
except ImportError as error:
    get_magnitude_along = error
try:
    from SciDataTool.Methods.Output.DataTime.get_phase_along import get_phase_along
except ImportError as error:
    get_phase_along = error
try:
    from SciDataTool.Methods.Output.DataTime.get_harmonics import get_harmonics
except ImportError as error:
    get_harmonics = error
try:
    from SciDataTool.Methods.Output.DataTime.get_nthoctave import get_nthoctave
except ImportError as error:
    get_nthoctave = error
try:
    from SciDataTool.Methods.Output.DataTime.find_periods import find_periods
except ImportError as error:
    find_periods = error
from numpy import array, array_equal
from SciDataTool.Classes._check import InitUnKnowClassError
from SciDataTool.Classes.Data import Data
class DataTime(DataND):
    """Class for physical quantities stored in the time/space domain"""
    VERSION = 1
    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Output.DataTime.get_axis
    if isinstance(get_axis, ImportError):
        get_axis = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataTime method get_axis: " + str(get_axis))
            )
        )
    else:
        get_axis = get_axis
    # cf Methods.Output.DataTime.get_FT_axis
    if isinstance(get_FT_axis, ImportError):
        get_FT_axis = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method get_FT_axis: " + str(get_FT_axis)
                )
            )
        )
    else:
        get_FT_axis = get_FT_axis
    # cf Methods.Output.DataTime.get_along
    if isinstance(get_along, ImportError):
        get_along = property(
            fget=lambda x: raise_(
                ImportError("Can't use DataTime method get_along: " + str(get_along))
            )
        )
    else:
        get_along = get_along
    # cf Methods.Output.DataTime.get_FT_along
    if isinstance(get_FT_along, ImportError):
        get_FT_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method get_FT_along: " + str(get_FT_along)
                )
            )
        )
    else:
        get_FT_along = get_FT_along
    # cf Methods.Output.DataTime.get_magnitude_along
    if isinstance(get_magnitude_along, ImportError):
        get_magnitude_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method get_magnitude_along: "
                    + str(get_magnitude_along)
                )
            )
        )
    else:
        get_magnitude_along = get_magnitude_along
    # cf Methods.Output.DataTime.get_phase_along
    if isinstance(get_phase_along, ImportError):
        get_phase_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method get_phase_along: " + str(get_phase_along)
                )
            )
        )
    else:
        get_phase_along = get_phase_along
    # cf Methods.Output.DataTime.get_harmonics
    if isinstance(get_harmonics, ImportError):
        get_harmonics = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method get_harmonics: " + str(get_harmonics)
                )
            )
        )
    else:
        get_harmonics = get_harmonics
    # cf Methods.Output.DataTime.get_nthoctave
    if isinstance(get_nthoctave, ImportError):
        get_nthoctave = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method get_nthoctave: " + str(get_nthoctave)
                )
            )
        )
    else:
        get_nthoctave = get_nthoctave
    # cf Methods.Output.DataTime.find_periods
    if isinstance(find_periods, ImportError):
        find_periods = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method find_periods: " + str(find_periods)
                )
            )
        )
    else:
        find_periods = find_periods
    # save method is available in all object
    save = save
    def __init__(
        self,
        axes=None,
        normalizations={},
        FTparameters={},
        values=None,
        symbol="",
        name="",
        unit="",
        symmetries={},
        init_dict=None,
    ):
        """Constructor of the class. Can be use in two ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for SciDataTool type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary wiht every properties as keys
        ndarray or list can be given for Vector and Matrix
        object or dict can be given for SciDataTool Object"""
        if init_dict is not None:  # Initialisation by dict
            check_init_dict(
                init_dict,
                [
                    "axes",
                    "normalizations",
                    "FTparameters",
                    "values",
                    "symbol",
                    "name",
                    "unit",
                    "symmetries",
                ],
            )
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
        # Initialisation by argument
        # Call DataND init
        super(DataTime, self).__init__(
            axes=axes,
            normalizations=normalizations,
            FTparameters=FTparameters,
            values=values,
            symbol=symbol,
            name=name,
            unit=unit,
            symmetries=symmetries,
        )
        # The class is frozen (in DataND init), for now it's impossible to
        # add new properties
    def __str__(self):
        """Convert this objet in a readeable string (for print)"""
        DataTime_str = ""
        # Get the properties inherited from DataND
        DataTime_str += super(DataTime, self).__str__() + linesep
        return DataTime_str
    def __eq__(self, other):
        """Compare two objects (skip parent)"""
        if type(other) != type(self):
            return False
        # Check the properties inherited from DataND
        if not super(DataTime, self).__eq__(other):
            return False
        return True
    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """
        # Get the properties inherited from DataND
        DataTime_dict = super(DataTime, self).as_dict()
        # The class name is added to the dict fordeserialisation purpose
        # Overwrite the mother class name
        DataTime_dict["__class__"] = "DataTime"
        return DataTime_dict
    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""
        # Set to None the properties inherited from DataND
        super(DataTime, self)._set_None()
