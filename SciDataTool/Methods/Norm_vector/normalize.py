from SciDataTool.Functions import NormError


def normalize(
    self,
    values,
):
    """Normalizes axis values
    Parameters
    ----------
    self: Norm_vector
        a Norm_vector object
    values: ndarray
        axis values
    Returns
    -------
    Vector of axis values
    """
    if len(values) != len(self.vector):
        raise NormError(
            "Normalization vector is not the same length as axis, cannot normalize"
        )
    else:
        return self.vector
