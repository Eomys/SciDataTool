import numpy as np


def union1d_tol(ar1, ar2, tol=1e-6, is_abs_tol=False, return_indices=False):
    """Return the intersect1d values of the input array a given tolerance tol

    Parameters
    ----------
    ar1 : ndarray
        First array to union values
    ar2 : ndarray
        Second array to union values
    tol : Float
        the tolerance value
    is_abs_tol : bool
        True to apply absolute tolerance regarding maximum absolute value in (ar1, ar2)
    return_indices : bool
        True to return indices

    Returns
    -------
    b : ndarray
        array containing unioned values
    Ia : ndarray
        index array such as ar1 = b[Ia]
    Ib : ndarray
        index array such as ar2 = b[Ib]
    """

    # Get union values as unique values in both arrays
    b = unique_tol(
        np.concatenate((ar1, ar2)),
        tol=tol,
        is_abs_tol=is_abs_tol,
        return_index=False,
        return_inverse=False,
    )

    if return_indices:
        # Map union values with values in 1st array
        Ia = np.argmin(np.abs(b[:, None] - ar1[None, :]), axis=0)
        # Map union values with values in 2nd array
        Ib = np.argmin(np.abs(b[:, None] - ar2[None, :]), axis=0)

        return b, Ia, Ib

    else:
        return b


def unique_tol(
    a,
    tol=1e-6,
    is_abs_tol=False,
    return_index=False,
    return_inverse=False,
    return_counts=False,
    is_stable=False,
    axis=0,
):
    """Return the unique values of the input array a given tolerance tol

    Parameters
    ----------
    a : ndarray
        the array to calculate unique values
    tol : Float
        the tolerance value
    is_abs_tol : bool
        True to apply absolute tolerance regarding maximum absolute value in a
    return_index : bool
        to return direct index
    return_inverse : bool
        to return inverse index
    return_counts : bool
        to return occurences count
    is_stable: bool
        to return unique array with stable order (not sorted)
    axis : int
        Axis index on which to calculate unique values

    Returns
    -------
    b : ndarray
        array containing unique values
    Ia : ndarray
        direct index array such as b=a[Ia] if is stable, else b=sort(a[Ia])
    Ib: ndarray
        inverse index array such as a=b[Ib]
    count0: ndarray
        array counting occurences for each unique value
    """

    if not is_abs_tol:
        tol = get_relative_tolerance(a, tol)

    res_tuple = np.unique(
        np.round(a / tol),
        return_index=True,
        return_inverse=return_inverse,
        return_counts=return_counts,
        axis=axis,
    )

    if is_stable:
        Ia = np.sort(res_tuple[1])
    else:
        Ia = res_tuple[1]

    b = a[Ia]

    if return_inverse:
        Ib = res_tuple[2]

    if return_counts:
        count0 = res_tuple[3]

    if return_index and return_inverse and return_counts:
        return b, Ia, Ib, count0
    elif return_index and return_inverse:
        return b, Ia, Ib
    elif return_index and return_counts:
        return b, Ia, count0
    elif return_inverse and return_counts:
        return b, Ib, count0
    elif return_index:
        return b, Ia
    elif return_inverse:
        return b, Ib
    elif return_counts:
        return b, count0
    else:
        return b


def intersect1d_tol(
    ar1, ar2, tol=1e-6, is_abs_tol=False, return_indices=False, assume_unique=False
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
    is_abs_tol : bool
        True to consider absolute tolerance, False to consider relative tolerance
    return_indices : bool
        True to return original indices for both input arrays
    assume_unique : bool
        True to assume values are unique in both input arrays

    Returns
    -------
    b : ndarray
        array containing common values
    Ia : ndarray
        array of indices such as b = ar1[Ia]
    Ib : ndarray
        array of indices such as b = ar2[Ib]
    """

    if not is_abs_tol:
        tol = get_relative_tolerance(ar1, tol)

    _, Ia, Ib = np.intersect1d(
        np.floor(ar1 / tol),
        np.floor(ar2 / tol),
        assume_unique=assume_unique,
        return_indices=True,
    )

    b = ar1[Ia]

    if return_indices:
        return b, Ia, Ib
    else:
        return b


def get_relative_tolerance(a, atol):
    """Calculate relative tolerance given an array a and an absolute tolerance

    Parameters
    ----------
    a : ndarray
        array for which to calculate relative tolerance
    atol : float
        absolute tolerance

    Returns
    -------
    rtol : float
        relative tolerance
    """

    a_max = np.max(np.abs(a))
    if a_max >= 0:
        rtol = atol * np.max(np.abs(a))

    if rtol > 1 or rtol == 0:
        # threshold tol to 1
        rtol = 1

    return rtol
