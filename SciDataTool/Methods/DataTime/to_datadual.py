def to_datadual(self, datafreq=None):
    """Creates a DataDual object.
    Parameters
    ----------
    self : DataTime
        a DataTime object
    datafreq : DataFreq
        a DataFreq object
    Returns
    -------
    a DataDual object
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataDual", fromlist=["DataDual"])
    DataDual = getattr(module, "DataDual")

    # Fill DataDual object with time/space data
    datadual = DataDual(
        name=self.name,
        symbol=self.symbol,
        unit=self.unit,
        normalizations=self.normalizations.copy(),
        axes_dt=self.axes,
        values_dt=self.values,
    )

    # Add fourier data (from input or using fft)
    if datafreq is None:
        datafreq = self.time_to_freq()
    datadual.axes_df = datafreq.axes
    datadual.values_df = datafreq.values

    return datadual
