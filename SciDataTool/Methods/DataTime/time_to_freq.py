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
    
    axes_str = []
    for i, axis in enumerate(self.axes):
        if axis.is_components:
            axis_str = axis.name + str(list(range(len(axis.values))))
        elif axis.name == "time":
            axis_str = "freqs"
        elif axis.name == "angle":
            axis_str = "wavenumber"
        else:
            axis_str = axis.name
        axes_str.append(axis_str)
    if axes_str == [axis.name for axis in self.axes]:
        raise AxisError(
            "ERROR: No available axis is compatible with fft (should be time or angle)"
        )
    else:
        results = self.get_along(*axes_str)
        values = results.pop(self.symbol)
        Axes = []
        for axis in self.axes:
            if axis.is_components: # components axis
                name = axis.name
                is_components = True
                axis_values = axis.values
                unit = "SI"
            elif axis.name == "time":
                name = "freqs"
                is_components = False
                axis_values = results["freqs"]
                unit = "Hz"
            elif axis.name == "angle":
                name = "wavenumber"
                is_components = False
                axis_values = results["wavenumber"]
                unit = "dimless"
            else:
                name = axis.name
                is_components = False
                axis_values = results[axis.name]
                unit = axis.unit
            Axes.append(Data1D(name=name, unit=unit, values=axis_values, is_components=is_components))
        return DataFreq(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=Axes,
            values=values,
        )