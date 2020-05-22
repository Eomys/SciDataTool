# -*- coding: utf-8 -*-
from SciDataTool import Data1D, DataFreq
from SciDataTool.Functions import AxisError

def time_to_freq(self):
    """Performs the Fourier Transform and stores the resulting field in a DataFreq object.
    Parameters
    ----------
    self : DataTime
        a DataTime object
    Returns
    -------
    FFT : DataFreq
        a DataFreq object
    """
    
    axes_str = []
    
    for axis in self.axes:
        if axis.name == "time":
            axes_str.append("freqs")
        elif axis.name == "angle":
            axes_str.append("wavenumber")
        
    if len(axes_str) == 1:
        if axes_str[0] == "freqs":
            (freqs, values) = self.get_FT_along("freqs")
            Freqs = Data1D(name="freqs", unit="Hz", values=freqs)
            return DataFreq(
                name=self.name,
                unit=self.unit,
                symbol=self.symbol,
                axes=[Freqs],
                values=values,
            )
        elif axes_str[0] == "wavenumber":
            (wavenumber, values) = self.get_FT_along("wavenumber")
            Wavenumber = Data1D(name="freqs", unit="dimless", values=wavenumber)
            return DataFreq(
                name=self.name,
                unit=self.unit,
                symbol=self.symbol,
                axes=[Wavenumber],
                values=values,
            )
    elif len(axes_str) == 2:
        (freqs, wavenumber, values) = self.get_FT_along("freqs", "wavenumber")
        Freqs = Data1D(name="freqs", unit="Hz", values=freqs)
        Wavenumber = Data1D(name="freqs", unit="dimless", values=wavenumber)
        return DataFreq(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=[Freqs, Wavenumber],
            values=values,
        )
    else:
        raise AxisError(
            "ERROR: No available axis is compatible with fft (time or angle)"
        )