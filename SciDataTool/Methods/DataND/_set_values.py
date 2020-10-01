# -*- coding: utf-8 -*-
from SciDataTool.Classes._check import check_dimensions, check_var
from numpy import squeeze

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
    
    # Check dimensions
    value = squeeze(value)
    value = check_dimensions(value, self.axes)
    self._values = value