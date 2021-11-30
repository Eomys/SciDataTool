import numpy as np


def union1d_tol(
    ar1,
    ar2,
    tol=1e-6,
    return_indices=False,
    return_union=True,
    is_abs_tol=False,
):
    """Return the intersect1d values of the input array a given tolerance tol

    Parameters
    ----------
    ar1 : ndarray
        First array to union values
    ar2 : ndarray
        Second array to union values
    tol : Float
        the tolerance value
    return_indices : bool
        True to return indices
    return_union : bool
        True to return union array
    is_abs_tol : bool
        True to apply absolute tolerance regarding maximum absolute value in (ar1, ar2)

    Returns
    -------
    result_dict : dictionary
        "union1d" is the array containing unioned values
        "un1" is the index array such as
        "un2" is the inverse index array such as
    """

    result_dict = dict()

    # Get union values as unique values in both arrays
    result_un = unique_tol(
        np.concatenate((ar1, ar2)),
        tol=tol,
        is_abs_tol=is_abs_tol,
        return_index=False,
        return_inverse=False,
    )

    if return_union:
        result_dict["union1d"] = result_un["b"]

    if return_indices:
        # Map union values with values in 1st array
        result_dict["un1"] = np.argmin(
            np.abs(result_un["b"][:, None] - ar1[None, :]), axis=0
        )
        # Map union values with values in 2nd array
        result_dict["un2"] = np.argmin(
            np.abs(result_un["b"][:, None] - ar2[None, :]), axis=0
        )

    return result_dict


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


def intersect1d_tol(
    ar1,
    ar2,
    tol=1e-6,
    assume_unique=False,
    return_indices=True,
    return_intersect=False,
    is_abs_tol=False,
):

    """Return the intersect1d values of the input array a given tolerance tol

    Parameters
    ----------
    ar1 : ndarray
        First array to intersect values
    ar2 : ndarray
        Second array to intersect values
    tol : Float
        the tolerance value
    assume_unique : bool
        True to assume values are unique in both input arrays
    return_indices : bool
        True to return original indices for both input arrays
    return_intersect : bool
        True to return interseced values of both arrays
    is_abs_tol : bool
        True to consider absolute tolerance, False to consider relative tolerance

    Returns
    -------
    result_dict : dictionary
        "intersect1d" is the array containing common values
        "comm1" is the index array such as
        "comm2" is the inverse index array such as
    """

    if is_abs_tol == False:
        tol = tol * np.max(np.abs(ar1))

    _, Ia, Ib = np.intersect1d(
        np.floor(ar1 / tol),
        np.floor(ar2 / tol),
        assume_unique=assume_unique,
        return_indices=True,
    )

    result_dict = dict()

    if return_intersect:
        result_dict["intersect1d"] = ar1[Ia]

    if return_indices:
        result_dict["comm1"] = Ia
        result_dict["comm2"] = Ib

    return result_dict
