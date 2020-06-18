# -*- coding: utf-8 -*-
"""File generated according to SciDataTool/Generator/ClassesRef/Output/Data.csv
WARNING! All changes made in this file will be lost!
"""
from os import linesep
from numpy import squeeze, array
from SciDataTool.Classes._check import check_init_dict, check_var, raise_
from SciDataTool.Functions.save import save
from SciDataTool.Classes._frozen import FrozenClass
from SciDataTool.Classes._check import InitUnKnowClassError

try:
    from SciDataTool.Methods.RequestedAxis.get_axis import get_axis
except ImportError as error:
    get_axis = error

class RequestedAxis(FrozenClass):
    """Class for handling of requested axis during get_along methods"""

    VERSION = 1
    # cf Methods.DataND.get_axis
    if isinstance(get_axis, ImportError):
        get_axis = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use RequestedAxis method get_axis: " + str(get_axis)
                )
            )
        )
    else:
        get_axis = get_axis
    # save method is available in all object
    save = save

    def __init__(
        self, name="", 
        corr_name="", 
        unit="", 
        corr_unit="",
        extension="", 
        values=None, 
        indices=None, 
        input_data=None, 
        operation=None, 
        index=None,
        transform=None,
    ):
        """Constructor of the class"""
        # Initialisation by argument
        self.name = name
        self.corr_name = corr_name
        self.unit = unit
        self.corr_unit = corr_unit
        self.extension = extension
        self.values = values
        self.indices = indices
        self.input_data = input_data
        self.operation = operation
        self.index = index
        self.transform = transform

