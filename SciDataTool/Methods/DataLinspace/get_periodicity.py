# -*- coding: utf-8 -*-


def get_periodicity(self):
    """Gives periodicity of the axis.
    Parameters
    ----------
    self: DataLinspace
        a DataLinspace object
    Returns
    -------
    per, is_antiper
    """

    per = 1
    is_antiper = False

    if self.name in self.symmetries:
        if "antiperiod" in self.symmetries.get(self.name):
            if self.symmetries.get(self.name)["antiperiod"] > 1:
                per = self.symmetries.get(self.name)["antiperiod"]
                is_antiper = True
        elif "period" in self.symmetries.get(self.name):
            if self.symmetries.get(self.name)["period"] > 1:
                per = self.symmetries.get(self.name)["period"]

    return (per, is_antiper)
