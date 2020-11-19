# -*- coding: utf-8 -*-
from SciDataTool.Functions import AxisError


def get_length(self, is_pattern=False):
    """Returns the length of the axis taking symmetries into account.
    Parameters
    ----------
    self: DataPattern
        a DataPattern object
    is_pattern: bool
        return length of pattern
    Returns
    -------
    Length of axis
    """

    if is_pattern:
        return len(self.values)
    else:
        return len(self.rebuild_indices)
