def get_axes(self, *args):
    """Returns the list of axes.
    Parameters
    ----------
    self: Data
        a Data object
    args : list
        list of axes names
    Returns
    -------
    axes_list : list of axes (Data)
    """

    axes = self.components[list(self.components.keys())[0]].axes

    if len(args) > 0:
        axes_list = []
        for name in args:
            for axis in axes:
                if axis.name == name:
                    axes_list.append(axis)
    else:
        axes_list = axes

    return axes_list
