import numpy as np


def unique_tol(
    a,
    tol=1e-6,
    return_index=False,
    return_inverse=False,
    return_counts=False,
    is_abs_tol=False,
    axis=0,
):

    """Return the unique values of the input array a given tolerance tol
    Python equivalent for MATLAB uniquetol function: https://fr.mathworks.com/help/matlab/ref/uniquetol.html

    Parameters
    ----------
    a : ndarray
        the array to calculate unique values
    tol : Float
        the tolerance value
    return_index : bool
        to return direct index
    return_inverse : bool
        to return inverse index
    return_counts : bool
        to return occurences count
    axis : int
        Axis index on which to calculate unique values

    Returns
    -------
    result_dict : dictionary
        "b" is the array containing unique values
        "Ia" is the index array such as b=a[Ia]
        "Ib" is the inverse index array such as a=b[Ib]
        "count0" is an array counting occurences for each unique value
    """

    if not is_abs_tol:
        a_max = np.max(np.abs(a))
        if a_max > 0:
            tol = tol * np.max(np.abs(a))

    if tol > 1:
        # threshold tol to 1
        tol = 1

    _, Ia, Ib, count0 = np.unique(
        np.round(a / tol),
        return_index=True,
        return_inverse=True,
        return_counts=True,
        axis=axis,
    )

    b = a[Ia]

    result_dict = dict()

    result_dict["b"] = b

    if return_inverse:
        result_dict["Ia"] = Ia

    if return_index:
        result_dict["Ib"] = Ib

    if return_counts:
        result_dict["count0"] = count0

    return result_dict
