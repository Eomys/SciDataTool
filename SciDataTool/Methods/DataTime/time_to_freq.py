# -*- coding: utf-8 -*-
from SciDataTool import Data1D
from SciDataTool.Functions import AxisError

def time_to_freq(self):
    """Performs the Fourier Transform and stores the resulting field in a DataFreq object.
    Parameters
    ----------
    self : DataTime
        a DataTime object
    Returns
    -------
    a DataFreq object
    """
    
    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataFreq", fromlist=["DataFreq"])
    DataFreq = getattr(module, "DataFreq")
    
    axes_str = [axis.name for axis in self.axes]
    axes_str = ["freqs" if axis_name == "time" else axis_name for axis_name in axes_str]
    axes_str = ["wavenumber" if axis_name == "angle" else axis_name for axis_name in axes_str]
    
    if axes_str == [axis.name for axis in self.axes]:
        raise AxisError(
            "ERROR: No available axis is compatible with fft (should be time or angle)"
        )
    else:
        results = self.get_along(*axes_str)
        values = results.pop(self.symbol)
        Axes = []
        for axis in results.keys():
            Axes.append(Data1D(name=axis, values=results[axis]))
        return DataFreq(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=Axes,
            values=values,
        )