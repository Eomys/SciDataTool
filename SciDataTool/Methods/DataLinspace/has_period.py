def has_period(self):
    """Indicates if an axis has symmetries.
    Parameters
    ----------
    self: DataLinspace
        a DataLinspace object
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
