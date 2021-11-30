def to_datadual(self, datatime=None):
    """Creates a DataDual object.
    Parameters
    ----------
    self : DataFreq
        a DataFreq object
    datatime : DataTime
        a DataTime object
    Returns
    -------
    a DataDual object
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataDual", fromlist=["DataDual"])
    DataDual = getattr(module, "DataDual")

    # Fill DataDual object with fourier data
    datadual = DataDual(
        name=self.name,
        symbol=self.symbol,
        unit=self.unit,
        normalizations=self.normalizations,
        axes_df=self.axes,
        values_df=self.values,
    )

    # Add time/space data (from input or using ifft)
    if datatime is None:
        datatime = self.freq_to_time()
    datadual.axes_dt = datatime.axes
    datadual.values_dt = datatime.values

    return datadual
