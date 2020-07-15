# -*- coding: utf-8 -*-
"""File generated according to SciDataTool/Generator/ClassesRef/Output/Data.csv
WARNING! All changes made in this file will be lost!
"""
from os import linesep
from SciDataTool.Classes._check import check_init_dict, check_var, raise_
from SciDataTool.Functions.save import save
from SciDataTool.Classes._frozen import FrozenClass
from SciDataTool.Classes._check import InitUnKnowClassError

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from SciDataTool.Methods.VectorField.get_rad_along import get_rad_along
except ImportError as error:
    get_rad_along = error

try:
    from SciDataTool.Methods.VectorField.get_tan_along import get_tan_along
except ImportError as error:
    get_tan_along = error

try:
    from SciDataTool.Methods.VectorField.get_ax_along import get_ax_along
except ImportError as error:
    get_ax_along = error

try:
    from SciDataTool.Methods.VectorField.get_rphiz_along import get_rphiz_along
except ImportError as error:
    get_rphiz_along = error
    
try:
    from SciDataTool.Methods.VectorField.get_mag_rad_along import get_mag_rad_along
except ImportError as error:
    get_mag_rad_along = error

try:
    from SciDataTool.Methods.VectorField.get_mag_tan_along import get_mag_tan_along
except ImportError as error:
    get_mag_tan_along = error

try:
    from SciDataTool.Methods.VectorField.get_mag_ax_along import get_mag_ax_along
except ImportError as error:
    get_mag_ax_along = error

try:
    from SciDataTool.Methods.VectorField.get_mag_rphiz_along import get_mag_rphiz_along
except ImportError as error:
    get_mag_rphiz_along = error
    
try:
    from SciDataTool.Methods.VectorField.get_harm_rad_along import get_harm_rad_along
except ImportError as error:
    get_harm_rad_along = error

try:
    from SciDataTool.Methods.VectorField.get_harm_tan_along import get_harm_tan_along
except ImportError as error:
    get_harm_tan_along = error

try:
    from SciDataTool.Methods.VectorField.get_harm_ax_along import get_harm_ax_along
except ImportError as error:
    get_harm_ax_along = error

try:
    from SciDataTool.Methods.VectorField.get_harm_rphiz_along import get_harm_rphiz_along
except ImportError as error:
    get_harm_rphiz_along = error


from SciDataTool.Classes._check import InitUnKnowClassError


class VectorField(FrozenClass):
    """Class for vector fields"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Simulation.VectorField.get_rad_along
    if isinstance(get_rad_along, ImportError):
        get_rad_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_rad_along: " + str(get_rad_along)
                )
            )
        )
    else:
        get_rad_along = get_rad_along
    # cf Methods.Simulation.VectorField.get_tan_along
    if isinstance(get_tan_along, ImportError):
        get_tan_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_tan_along: " + str(get_tan_along)
                )
            )
        )
    else:
        get_tan_along = get_tan_along
    # cf Methods.Simulation.VectorField.get_ax_along
    if isinstance(get_ax_along, ImportError):
        get_ax_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_ax_along: " + str(get_ax_along)
                )
            )
        )
    else:
        get_ax_along = get_ax_along
    # cf Methods.Simulation.VectorField.get_rphiz_along
    if isinstance(get_rphiz_along, ImportError):
        get_rphiz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_rphiz_along: " + str(get_rphiz_along)
                )
            )
        )
    else:
        get_rphiz_along = get_rphiz_along
    # cf Methods.Simulation.VectorField.get_mag_rad_along
    if isinstance(get_mag_rad_along, ImportError):
        get_mag_rad_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_mag_rad_along: " + str(get_mag_rad_along)
                )
            )
        )
    else:
        get_mag_rad_along = get_mag_rad_along
    # cf Methods.Simulation.VectorField.get_mag_tan_along
    if isinstance(get_mag_tan_along, ImportError):
        get_mag_tan_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_mag_tan_along: " + str(get_mag_tan_along)
                )
            )
        )
    else:
        get_mag_tan_along = get_mag_tan_along
    # cf Methods.Simulation.VectorField.get_mag_ax_along
    if isinstance(get_mag_ax_along, ImportError):
        get_mag_ax_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_mag_ax_along: " + str(get_mag_ax_along)
                )
            )
        )
    else:
        get_mag_ax_along = get_mag_ax_along
    # cf Methods.Simulation.VectorField.get_mag_rphiz_along
    if isinstance(get_mag_rphiz_along, ImportError):
        get_mag_rphiz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_mag_rphiz_along: " + str(get_mag_rphiz_along)
                )
            )
        )
    else:
        get_mag_rphiz_along = get_mag_rphiz_along
    # cf Methods.Simulation.VectorField.get_mag_rad_along
    if isinstance(get_harm_rad_along, ImportError):
        get_harm_rad_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_harm_rad_along: " + str(get_harm_rad_along)
                )
            )
        )
    else:
        get_harm_rad_along = get_harm_rad_along
    # cf Methods.Simulation.VectorField.get_harm_tan_along
    if isinstance(get_harm_tan_along, ImportError):
        get_harm_tan_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_harm_tan_along: " + str(get_harm_tan_along)
                )
            )
        )
    else:
        get_harm_tan_along = get_harm_tan_along
    # cf Methods.Simulation.VectorField.get_harm_ax_along
    if isinstance(get_harm_ax_along, ImportError):
        get_harm_ax_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_harm_ax_along: " + str(get_harm_ax_along)
                )
            )
        )
    else:
        get_harm_ax_along = get_harm_ax_along
    # cf Methods.Simulation.VectorField.get_harm_rphiz_along
    if isinstance(get_harm_rphiz_along, ImportError):
        get_harm_rphiz_along = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use VectorField method get_harm_rphiz_along: " + str(get_harm_rphiz_along)
                )
            )
        )
    else:
        get_harm_rphiz_along = get_harm_rphiz_along
    # save method is available in all object
    save = save

    # generic copy method
    def copy(self):
        """Return a copy of the class
        """
        return type(self)(init_dict=self.as_dict())

    def __init__(self, name="", symbol="", components={}, init_dict = None, init_str = None):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for pyleecan type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with every properties as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "components" in list(init_dict.keys()):
                components = init_dict["components"]
        # Initialisation by argument
        self.parent = None
        self.name = name
        self.symbol = symbol
        self.components = components

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        VectorField_str = ""
        if self.parent is None:
            VectorField_str += "parent = None " + linesep
        else:
            VectorField_str += "parent = " + str(type(self.parent)) + " object" + linesep
        VectorField_str += 'name = "' + str(self.name) + '"' + linesep
        VectorField_str += "components = " + str(self.components) + linesep
        return VectorField_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.name != self.name:
            return False
        if other.components != self.components:
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        VectorField_dict = dict()
        VectorField_dict["name"] = self.name
        VectorField_dict["components"] = self.components
        # The class name is added to the dict fordeserialisation purpose
        VectorField_dict["__class__"] = "VectorField"
        return VectorField_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.name = None
        self.components = None

    def _get_name(self):
        """getter of name"""
        return self._name

    def _set_name(self, value):
        """setter of name"""
        check_var("name", value, "str")
        self._name = value

    # Name of the vector field
    # Type : str
    name = property(
        fget=_get_name, fset=_set_name, doc=u"""Name of the vector field"""
    )
    
    def _get_symbol(self):
        """getter of symbol"""
        return self._symbol

    def _set_symbol(self, value):
        """setter of symbol"""
        check_var("symbol", value, "str")
        self._symbol = value

    # Symbol of the vector field
    # Type : str
    symbol = property(
        fget=_get_symbol, fset=_set_symbol, doc=u"""Symbol of the vector field"""
    )

    def _get_components(self):
        """getter of components"""
        return self._components

    def _set_components(self, value):
        """setter of components"""
        check_var("components", value, "dict")
        self._components = value

    # Dict of the components
    # Type : dict
    components = property(
        fget=_get_components, fset=_set_components, doc=u"""Dict of the components"""
    )