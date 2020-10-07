# -*- coding: utf-8 -*-
from SciDataTool import Data1D
from SciDataTool.Functions import AxisError


def freq_to_time(self):
    """Performs the inverse Fourier Transform and stores the resulting field in a DataTime object.
    Parameters
    ----------
    self : DataFreq
        a DataFreq object
    Returns
    -------
    a DataTime object
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataTime", fromlist=["DataTime"])
    DataTime = getattr(module, "DataTime")

    axes_str = []
    for i, axis in enumerate(self.axes):
        if axis.is_components:
            axis_str = axis.name + str(list(range(len(axis.values))))
        elif axis.name == "freqs":
            axis_str = "time"
        elif axis.name == "wavenumber":
            axis_str = "angle"
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
            if axis.is_components:  # components axis
                name = axis.name
                is_components = True
                axis_values = axis.values
                unit = "SI"
            elif axis.name == "freqs":
                name = "time"
                is_components = False
                axis_values = results["time"]
                unit = "s"
            elif axis.name == "wavenumber":
                name = "angle"
                is_components = False
                axis_values = results["angle"]
                unit = "rad"
            else:
                name = axis.name
                is_components = False
                axis_values = results[axis.name]
                unit = axis.unit
            Axes.append(
                Data1D(
                    name=name,
                    unit=unit,
                    values=axis_values,
                    is_components=is_components,
                )
            )
        return DataTime(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=Axes,
            values=values,
        )
