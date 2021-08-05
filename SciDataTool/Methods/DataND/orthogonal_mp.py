# -*- coding: utf-8 -*-

import numpy as np

from typing import Dict, List
from numpy import ndarray
from SciDataTool.Classes.Data1D import Data1D
from SciDataTool.Functions.omp import omp, comp_undersampled_axe

# To prevent circular import
#from SciDataTool.Classes.DataND import DataND as sdt_DataND

def orthogonal_mp(self, Time: Data1D, n_coefs: int=None):
    """
    Execute the Orthogonal Matching Pursuit on each components provided
    
    Parameter
    ---------

    components: List of components of the DataND object, if empty the OMP is executed on all components
    axe: List of Data1D object on which the components are recovered
    M: List of undersampling index, the time axes of the self.components are the elements axe[M]

    Returns
    recovered_dataND: A new dataND object composed of the recovered components
    """

    # This method should only be used for 1D or 2D field, where the
    # undersampling is in the direction of time
    nombre_axes = len(self.axes)
    assert nombre_axes == 2 or nombre_axes == 1, "Dimension error: {} not in {1,2}".format(nombre_axes)

    axes_name = [self.axes[i].name for i in range(nombre_axes)]
    assert "time" in axes_name, "There is no time axe"
    axes_name.remove("time")

    # Extract the axes
    if nombre_axes == 2:
        [Angle] = self.get_axes(axes_name[0])
    [Time_undersampled] = self.get_axes("time")

    M = comp_undersampled_axe(Time_undersampled,Time)

    n = len(Time.values)

    # Stack the signals into the columns of the matrix Y (n,n_targets)
    Y = self.values

    # Compute the OMP
    Y_full = omp(Y,M,n,n_coefs=n_coefs)

    # Build the DataND object
    if nombre_axes == 1:
        recovered_dataND = type(self)(
            name=self.name,
            symbol=self.symbol,
            unit=self.unit,
            axes=[Time],
            values=Y_full,
            is_real=self.is_real,
        )
    if nombre_axes == 2:
        recovered_dataND = type(self)(
            name=self.name,
            symbol=self.symbol,
            unit=self.unit,
            axes=[Time,Angle],
            values=Y_full,
            is_real=self.is_real,
        )

    return recovered_dataND














