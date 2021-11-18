from SciDataTool.Methods.DataDual import is_freq


def get_along(
    self,
    *args,
    unit="SI",
    is_norm=False,
    axis_data=[],
    is_squeeze=True,
    is_magnitude=False
):
    """Returns the ndarray of the field, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    axis_data: list
        list of ndarray corresponding to user-input data
    Returns
    -------
    list of 1Darray of axes values, ndarray of field values
    """

    # Get best attributes (time/space or fourier)
    if is_freq(*args):
        if hasattr(self, "values_df") and self.values_df is not None:
            # Replace axes and values with fourier ones
            self.axes = self.axes_df
            self.values = self.values_df
        else:
            # Replace axes and values with time/space ones
            self.axes = self.axes_dt
            self.values = self.values_dt
    else:
        if hasattr(self, "values_dt") and self.values_dt is not None:
            # Replace axes and values with time/space ones
            self.axes = self.axes_dt
            self.values = self.values_dt
        else:
            # Replace axes and values with fourier ones
            self.axes = self.axes_df
            self.values = self.values_df

    # Call DataND.get_along()
    return super(type(self), self).get_along(
        *args,
        unit=unit,
        is_norm=is_norm,
        axis_data=axis_data,
        is_squeeze=is_squeeze,
        is_magnitude=is_magnitude
    )
