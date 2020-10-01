# -*- coding: utf-8 -*-
from SciDataTool.Classes._check import check_dimensions
from numpy import squeeze

def _set_values(self, value):
    """Returns the values of the field interpolated over the axes values.
    Parameters
    ----------
    self: Data
        a Data object
    values: ndarray
        array of the field
    axes_list: list
        a list of RequestedAxis objects
    Returns
    -------
    values: ndarray
        values of the field
    """
    
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