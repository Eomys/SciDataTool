def has_period(self):
    """Indicates if an axis has symmetries.
    Parameters
    ----------
    self: Data1D
        a Data1D object
    Returns
    -------
    Boolean
    """
    answer = False

    if "antiperiod" in self.symmetries:
        if self.symmetries["antiperiod"] > 1:
            answer = True
    elif "period" in self.symmetries:
        if self.symmetries["period"] > 1:
            answer = True

    return answer
