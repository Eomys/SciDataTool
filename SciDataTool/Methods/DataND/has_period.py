# -*- coding: utf-8 -*-


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

    if self.symmetries != {}:
        answer = True

    return answer
