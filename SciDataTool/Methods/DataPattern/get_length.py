def get_length(self, is_pattern=False, is_smallestperiod=False):
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
    if is_smallestperiod:
        return len(self.values)
    elif is_pattern:
        return len(self.values)
    else:
        return len(self.rebuild_indices)
