# -*- coding: utf-8 -*-
from SciDataTool import Data1D, DataTime
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
    
    axes_str = []
    
    for axis in self.axes:
        if axis.name == "freqs":
            axes_str.append("time")
        elif axis.name == "wavenumber":
            axes_str.append("angle")
        
    if len(axes_str) == 1:
        if axes_str[0] == "time":
            (time, values) = self.get_FT_along("time")
            Time = Data1D(name="time", unit="s", values=time)
            return DataTime(
                name=self.name,
                unit=self.unit,
                symbol=self.symbol,
                axes=[Time],
                values=values,
            )
        elif axes_str[0] == "angle":
            (angle, values) = self.get_FT_along("angle")
            Angle = Data1D(name="angle", unit="rad", values=angle)
            return DataTime(
                name=self.name,
                unit=self.unit,
                symbol=self.symbol,
                axes=[Angle],
                values=values,
            )
    elif len(axes_str) == 2:
        (time, angle, values) = self.get_FT_along("time", "wavenumber")
        Time = Data1D(name="time", unit="s", values=time)
        Angle = Data1D(name="angle", unit="rad", values=angle)
        return DataTime(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=[Time, Angle],
            values=values,
        )
    else:
        raise AxisError(
            "ERROR: No available axis is compatible with fft (should be freqs or wavenumber)"
        )