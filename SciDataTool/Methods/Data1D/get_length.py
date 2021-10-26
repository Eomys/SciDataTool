from SciDataTool.Functions import AxisError


def get_length(self, is_oneperiod=False, is_antiperiod=False, is_smallestperiod=False):
    """Returns the length of the axis taking symmetries into account.
    Parameters
    ----------
    self: Data1D
        a Data1D object
    is_oneperiod: bool
        return values on a single period
    is_antiperiod: bool
        return values on a semi period (only for antiperiodic signals)
    Returns
    -------
    Length of axis
    """
    N = len(self.values)
    # Rebuild symmetries
    if is_smallestperiod:
        return N
    elif is_antiperiod:
        if "antiperiod" in self.symmetries:
            return N
        else:
            raise AxisError("axis has no antiperiodicity")
    elif is_oneperiod:
        if "antiperiod" in self.symmetries:
            return N * 2
        elif "period" in self.symmetries:
            return N
        else:
            return N
    else:
        if "antiperiod" in self.symmetries:
            return N * self.symmetries["antiperiod"]
        elif "period" in self.symmetries:
            return N * self.symmetries["period"]
        else:
            return N
