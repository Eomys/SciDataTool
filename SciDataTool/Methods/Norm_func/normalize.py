def normalize(
    self,
    values,
):
    """Normalizes axis values
    Parameters
    ----------
    self: Norm_func
        a Norm_func object
    values: ndarray
        axis values
    Returns
    -------
    Vector of axis values
    """
    return self.function(values)
