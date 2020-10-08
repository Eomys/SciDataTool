# -*- coding: utf-8 -*-


def get_axes(self):
    """Returns the list of axes.
    Parameters
    ----------
    self: Data
        a Data object
    Returns
    -------
    list of axes (Data)
    """

    return self.components[list(self.components.keys())[0]].axes
