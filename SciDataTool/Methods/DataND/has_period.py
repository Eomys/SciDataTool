def has_period(self):
    """Indicates if a field has symmetries.
    Parameters
    ----------
    self: DataND
        a DataND object
    Returns
    -------
    Boolean
    """
    answer = False

    for axis in self.axes:

        if axis.symmetries != {}:
            answer = True

    return answer
