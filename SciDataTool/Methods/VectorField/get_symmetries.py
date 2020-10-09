# -*- coding: utf-8 -*-


def get_symmetries(self):
    """Returns the dict of symmetries.
    Parameters
    ----------
    self: Data
        a Data object
    Returns
    -------
    dict of symmetries
    """

    return self.components[list(self.components.keys())[0]].symmetries
