from SciDataTool.Classes.Data1D import Data1D

import numpy as np
from numpy import (
    ndarray,
    concatenate,
    identity,
    arange,
    asarray,
    sin,
    pi,
    outer,
    linspace,
    sqrt,
)
from sklearn.linear_model import orthogonal_mp
from scipy.fft import idct
from math import floor


def comp_DST(n: int) -> ndarray:
    """
    Compute the matrix of sinusoids, stacked as the columns of DST, with normed columns
    The first null component is removed because it would
    be redondant with the first component of the DCT's matrix.

    Return:
    DST: ndarray of shape (n,n-1)
    """

    f = 0.5 * arange(n)
    t = linspace(0, 1, n, endpoint=False)

    DST = sin(2 * pi * outer(f, t))

    # Norm the columns
    DST = 2 * (1 / sqrt(2 * n)) * DST

    # Remove the first null component
    DST = DST[:, 1:]

    return DST


def comp_undersampling(K: float, Time: Data1D, seed: int = 42) -> ndarray:
    """
    Compute an undersampled Data1D object with a percentage K of the initial samples

    Parameters
    ----------
    K: 0 <= K <= 1
    Time: Data1D object which is undersample
    seed: integer used to initialize the numpy's random generator

    Returns:
    M: ndarray containing the indices of the observed samples of Time
    Time_under: The undersampled version of the Time Data1D object
    """

    assert K <= 1 and K >= 0, "K = {} is not a percentage".format(K)

    n = len(Time.values)
    m = floor(K * n)

    np.random.seed(seed)
    M = np.random.choice(n, m, replace=False)
    M.sort()
    M = asarray(M)

    time_under = Time.values[M]

    Time_under = Data1D(
        name=Time.name,
        unit=Time.unit,
        values=time_under,
    )

    return M, Time_under


def comp_dictionary(n: int, M: ndarray) -> ndarray:
    """
    Construct the dictionary on which the signal is decomposed

    Parameters
    ----------
    n: length of the time vector
    M: index of the grid corresponding to the observations of the undersampled signal

    Returns
    dictionary: concatenation of the DST and DCT's matrix
    """

    DCT = idct(identity(n), type=2, norm="ortho", axis=0)
    DCT = DCT[M]

    # DST with normed columns
    # The first null component is removed in comp_DST
    DST = comp_DST(n)
    DST = DST[M]

    dictionary = concatenate([DCT, DST], axis=1)

    return dictionary


def comp_undersampled_axe(Time: Data1D, Time_under: Data1D) -> ndarray:
    """
    Compute the ndarray M of indices of the undersampled signal such that:
    Time_under.value = Time.value[M]

    This funtion assumes the elements of Time_under.value are elements of Time.value
    """

    # Extract the ndarray time vectors
    time_under = Time_under.values
    time = Time.values

    # Element wise comparison and selection of indices
    M = np.arange(len(time))
    M = M[np.isin(time, time_under)]

    return M


def omp(
    Y: ndarray,
    M: ndarray,
    n: int,
    n_coefs: int = None,
    precompute: bool = True,
    dictionary=None,
    return_path: bool = False,
) -> ndarray:
    """
    Given Y of shape (len(M),n_targets), recover n_targets signals (of length len(M)) with joint sparsity.
    Each signal - column of Y - is the signal's observation on the support M

    Parameter
    ---------
    Y: ndarray (len(M),n_targets) matrix of the n_targets joint sparse signals.
    M: index of the grid corresponding to the observations of the signals.
    n: length of the grid on which the signal is undersampled.
    n_coefs: passed to n_nonzero_coefs, a parameter of orthogonal_mp. It's the number of atoms
    of the dictionary used to decomposed the signals. If None set to 10% of n.
    precompute: whether to precompute. Improves performance for large Y.

    Returns:
    Y_full: ndarray (n,n_targets) matrix of the recovered signals

    """

    if dictionary is None:
        dictionary_decomp = comp_dictionary(n, M)
    else:
        dictionary_decomp = dictionary[0]
        dictionary_synth = dictionary[1]

    # Compute the sparse decomposition of the signals with the scikit-learn
    # This implementation can only be used on real-valued signals, it uses a Cholesky factorization

    if return_path:
        sparse_decomposition, n_iters = orthogonal_mp(
            X=dictionary_decomp,
            y=Y,
            n_nonzero_coefs=n_coefs,
            precompute=precompute,
            return_path=return_path,
        )
    else:
        sparse_decomposition = orthogonal_mp(
            X=dictionary_decomp, y=Y, n_nonzero_coefs=n_coefs, precompute=precompute
        )

    dictionary_synth = comp_dictionary(n, arange(n))

    Y_full = dictionary_synth @ sparse_decomposition

    if return_path:
        return Y_full, n_iters
    else:
        return Y_full
