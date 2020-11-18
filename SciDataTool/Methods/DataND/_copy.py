# -*- coding: utf-8 -*-
from SciDataTool.Classes._check import check_dimensions, check_var
from numpy import squeeze, array
from copy import deepcopy


def _copy(self):
    """copy object"""
    
    return self.deepcopy()
