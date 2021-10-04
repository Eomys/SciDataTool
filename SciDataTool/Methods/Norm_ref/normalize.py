def normalize(
    self,
    values,
):
    """Normalizes axis values
    Parameters
    ----------
    self: Norm_ref
        a Norm_ref object
    values: ndarray
        axis values
    Returns
    -------
    Vector of axis values
    """
    return values / self.ref
