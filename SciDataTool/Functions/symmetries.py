from SciDataTool.Functions import AxisError
from numpy import tile, concatenate, negative, ones, append


def rebuild_symmetries(values, axis_index, symmetries):
    """Reconstructs the field of a Data object taking symmetries into account
    Parameters
    ----------
    values: ndarray
        ndarray of a field
    axis_index: int
        Index of the axis along which the symmetry is made
    symmetries: dict
        Dictionary of the symmetries along one axis
    Returns
    -------
    ndarray of the reconstructed field
    """
    if "period" in symmetries.keys():
        values = mytile(values, symmetries.get("period"), axis_index)
    elif "antiperiod" in symmetries.keys():
        values2 = concatenate((values, negative(values)), axis=axis_index)
        values3 = mytile(values2, symmetries.get("antiperiod") // 2, axis_index)
        if symmetries.get("antiperiod") % 2 == 1:
            values = concatenate((values3, values), axis=axis_index)
        else:
            values = values3
    return values


def rebuild_symmetries_axis(values, symmetries):
    """Reconstructs the field of a Data object taking symmetries into account
    Parameters
    ----------
    values: ndarray
        ndarray of a the axis values
    symmetries: dict
        Dictionary of the symmetries along the axis
    Returns
    -------
    ndarray of the reconstructed axis
    """
    values_new = values
    if "period" in symmetries.keys():
        for i in range(symmetries.get("period") - 1):
            if len(values) == 1:
                if "delta" in symmetries.keys():
                    values_new = append(
                        values_new, values_new[-1] + symmetries["delta"]
                    )
                else:
                    raise AxisError("must provide delta for symmetries with one sample")
            else:
                values_new = concatenate(
                    (
                        values_new,
                        values + (values_new[-1] - values_new[-2]) + values_new[-1],
                    )
                )
    elif "antiperiod" in symmetries.keys():
        for i in range(symmetries.get("antiperiod") - 1):
            if len(values) == 1:
                if "delta" in symmetries.keys():
                    values_new = append(
                        values_new, values_new[-1] + symmetries["delta"]
                    )
                else:
                    raise AxisError("must provide delta for symmetries with one sample")
            else:
                values_new = concatenate(
                    (
                        values_new,
                        values + (values_new[-1] - values_new[-2]) + values_new[-1],
                    )
                )
    return values_new


def mytile(values, n, axis_index):
    values_shape = values.shape
    reps = ones(len(values_shape), dtype=int)
    reps[axis_index] = n
    return tile(values, reps)
