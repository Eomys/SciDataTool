# -*- coding: utf-8 -*-


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

    if self.name in self.symmetries:
        if "antiperiod" in self.symmetries.get(self.name):
            if self.symmetries.get(self.name)["antiperiod"] > 1:
                answer = True
        elif "period" in self.symmetries.get(self.name):
            if self.symmetries.get(self.name)["period"] > 1:
                answer = True

    return answer
