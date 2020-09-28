# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Data/DataLinspace.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//DataLinspace
"""

from os import linesep
from logging import getLogger
from ._check import check_var, raise_
from ..Functions.save import save
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Data import Data

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.DataLinspace.get_values import get_values
except ImportError as error:
    get_values = error


from ._check import InitUnKnowClassError


class DataLinspace(Data):
    """Class for axes defined as linspaces"""

    VERSION = 1

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
    # save method is available in all object
    save = save

    # generic copy method
    def copy(self):
        """Return a copy of the class
        """
        return type(self)(init_dict=self.as_dict())

    def __init__(self, initial=None, final=None, step=None, number=None, include_endpoint=True, is_components=False, symbol="", name="", unit="", symmetries=-1, init_dict = None, init_str = None):
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
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
        # Set the properties (value check and convertion are done in setter)
        self.initial = initial
        self.final = final
        self.step = step
        self.number = number
        self.include_endpoint = include_endpoint
        self.is_components = is_components
        # Call Data init
        super(DataLinspace, self).__init__(symbol=symbol, name=name, unit=unit, symmetries=symmetries)
        # The class is frozen (in Data init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        DataLinspace_str = ""
        # Get the properties inherited from Data
        DataLinspace_str += super(DataLinspace, self).__str__()
        DataLinspace_str += "initial = " + str(self.initial) + linesep
        DataLinspace_str += "final = " + str(self.final) + linesep
        DataLinspace_str += "step = " + str(self.step) + linesep
        DataLinspace_str += "number = " + str(self.number) + linesep
        DataLinspace_str += "include_endpoint = " + str(self.include_endpoint) + linesep
        DataLinspace_str += "is_components = " + str(self.is_components) + linesep
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
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        # Get the properties inherited from Data
        DataLinspace_dict = super(DataLinspace, self).as_dict()
        DataLinspace_dict["initial"] = self.initial
        DataLinspace_dict["final"] = self.final
        DataLinspace_dict["step"] = self.step
        DataLinspace_dict["number"] = self.number
        DataLinspace_dict["include_endpoint"] = self.include_endpoint
        DataLinspace_dict["is_components"] = self.is_components
        # The class name is added to the dict fordeserialisation purpose
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
        doc=u"""Boolean indicating if the endpoint must be included

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
        doc=u"""Boolean inidcating if the axis is components

        :Type: bool
        """,
    )
