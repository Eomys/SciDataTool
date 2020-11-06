# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/VectorField.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//VectorField
"""

from os import linesep
from ._check import check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from ._frozen import FrozenClass

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.VectorField.get_rphiz_along import get_rphiz_along
except ImportError as error:
    get_rphiz_along = error

try:
    from ..Methods.VectorField.get_xyz_along import get_xyz_along
except ImportError as error:
    get_xyz_along = error

try:
    from ..Methods.VectorField.get_mag_rphiz_along import get_mag_rphiz_along
except ImportError as error:
    get_mag_rphiz_along = error

try:
    from ..Methods.VectorField.get_mag_xyz_along import get_mag_xyz_along
except ImportError as error:
    get_mag_xyz_along = error

try:
    from ..Methods.VectorField.get_harm_rphiz_along import get_harm_rphiz_along
except ImportError as error:
    get_harm_rphiz_along = error

try:
    from ..Methods.VectorField.get_harm_xyz_along import get_harm_xyz_along
except ImportError as error:
    get_harm_xyz_along = error

try:
    from ..Methods.VectorField.get_axes import get_axes
except ImportError as error:
    get_axes = error


from ._check import InitUnKnowClassError


class VectorField(FrozenClass):
    """Class for 2D or 3D vector fields (time or frequency domain)"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
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
    # cf Methods.VectorField.get_axes
    if isinstance(get_axes, ImportError):
        get_axes = property(
            fget=lambda x: raise_(
                ImportError("Can't use VectorField method get_axes: " + str(get_axes))
            )
        )
    else:
        get_axes = get_axes
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(
        self, name="", symbol="", components=-1, init_dict=None, init_str=None
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

    def as_dict(self):
        """Convert this object in a json seriable dict (can be use in __init__)"""

        VectorField_dict = dict()
        VectorField_dict["name"] = self.name
        VectorField_dict["symbol"] = self.symbol
        if self.components is None:
            VectorField_dict["components"] = None
        else:
            VectorField_dict["components"] = dict()
            for key, obj in self.components.items():
                VectorField_dict["components"][key] = obj.as_dict()
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
