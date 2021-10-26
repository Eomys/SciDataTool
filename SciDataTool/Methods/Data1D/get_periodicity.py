def get_periodicity(self):
    """Gives periodicity of the axis.
    Parameters
    ----------
    self: Data1D
        a Data1D object
    Returns
    -------
    per, is_antiper
    """

    per = 1
    is_antiper = False

    if "antiperiod" in self.symmetries:
        if self.symmetries["antiperiod"] > 1:
            per = self.symmetries["antiperiod"]
            is_antiper = True
    elif "period" in self.symmetries:
        if self.symmetries["period"] > 1:
            per = self.symmetries["period"]

    return (per, is_antiper)
