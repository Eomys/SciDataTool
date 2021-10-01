def normalize(
    self,
    values,
):
    """Normalizes axis values
    Parameters
    ----------
    self: Norm_affine
        a Norm_affine object
    values: ndarray
        axis values
    Returns
    -------
    Vector of axis values
    """
    return values * self.slope + self.offset
