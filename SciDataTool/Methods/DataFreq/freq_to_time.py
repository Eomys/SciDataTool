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
    module = __import__("SciDataTool.Classes.DataPattern", fromlist=["DataPattern"])
    DataPattern = getattr(module, "DataPattern")

    axes_str = []
    for i, axis in enumerate(self.axes):
        if axis.is_components:
            axis_str = axis.name + str(list(range(len(axis.values))))
        elif axis.name == "freqs":
            axis_str = "time[smallestperiod]"
        elif axis.name == "wavenumber":
            axis_str = "angle[smallestperiod]"
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
            if axis.name == "freqs":
                axis_new = Data1D(
                    name="time",
                    is_components=False,
                    values=results["time"],
                    unit="s",
                    symmetries=axis.symmetries.copy(),
                    normalizations=axis.normalizations.copy(),
                )
            elif axis.name == "wavenumber":
                axis_new = Data1D(
                    name="angle",
                    is_components=False,
                    values=results["angle"],
                    unit="rad",
                    symmetries=axis.symmetries.copy(),
                    normalizations=axis.normalizations.copy(),
                )
            else:
                axis_new = axis.copy()
            Axes.append(axis_new)

        return DataTime(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=Axes,
            values=values,
            is_real=self.is_real,
            normalizations=self.normalizations.copy(),
        )
