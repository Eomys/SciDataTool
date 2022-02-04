def get_axes(self, *args):
    """Returns the list of axes.
    Parameters
    ----------
    self: DataDual
        a DataDual object
    args : list
        list of axes names
    Returns
    -------
    axes_list : list of axes (Data)
    """

    if self.axes is None:
        axes = self.axes_dt + self.axes_df
    else:
        axes = self.axes

    if len(args) > 0:
        axes_list = []
        for name in args:
            for axis in axes:
                if axis.name == name:
                    axes_list.append(axis)
    else:
        axes_list = axes

    return axes_list
