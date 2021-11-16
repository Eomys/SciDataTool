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
    module = __import__("SciDataTool.Classes.DataPattern", fromlist=["DataPattern"])
    DataPattern = getattr(module, "DataPattern")

    axes_str = []
    for i, axis in enumerate(self.axes):
        if axis.is_components:
            axis_str = axis.name + str(list(range(len(axis.values))))
        elif axis.name == "time":
            axis_str = "freqs"
        elif axis.name == "angle":
            axis_str = "wavenumber"
        elif isinstance(axis, DataPattern):
            axis_str = axis.name + "[pattern]"
        else:
            axis_str = axis.name + "[smallestperiod]"
        axes_str.append(axis_str)
    if axes_str == [axis.name for axis in self.axes]:
        raise AxisError(
            "No available axis is compatible with fft (should be time or angle)"
        )
    else:
        results = self.get_along(*axes_str)
        values = results.pop(self.symbol)
        Axes = []
        for axis in self.axes:
            if axis.name == "time":
                if "antiperiod" in axis.symmetries:
                    symmetries = {"period": int(axis.symmetries["antiperiod"] / 2)}
                else:
                    symmetries = axis.symmetries.copy()
                axis_new = Data1D(
                    name="freqs",
                    is_components=False,
                    values=results["freqs"],
                    unit="Hz",
                    symmetries=symmetries,
                    normalizations=axis.normalizations.copy(),
                ).to_linspace()
            elif axis.name == "angle":
                if "antiperiod" in axis.symmetries:
                    symmetries = {"period": int(axis.symmetries["antiperiod"] / 2)}
                else:
                    symmetries = axis.symmetries.copy()
                axis_new = Data1D(
                    name="wavenumber",
                    is_components=False,
                    values=results["wavenumber"],
                    unit="dimless",
                    symmetries=symmetries,
                    normalizations=axis.normalizations.copy(),
                ).to_linspace()
            else:
                axis_new = axis.copy()
            Axes.append(axis_new)
        return DataFreq(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=Axes,
            values=values,
            is_real=self.is_real,
            normalizations=self.normalizations.copy(),
        )
