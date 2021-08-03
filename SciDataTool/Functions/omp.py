from logging import getLogger

import numpy as np
from numpy import ndarray, concatenate, identity, arange
from sklearn.linear_model import orthogonal_mp
from scipy.fft import idct, idst


def comp_dictionary(n: int, M: ndarray) -> ndarray:
    """
    Construct the dictionary on which the signal is decomposed

    Parameter
    ---------

    M: index of the grid corresponding to the observations of the signal
    n: length of the grid on which the signal is undersampled


    Returns
    dictionary: concatenation of the DST and DCT's matrix
    """

    DCT = idct(identity(n), type=2, norm='ortho', axis=0)
    DCT = DCT[M]
    DST = idst(identity(n), type=2, norm='ortho', axis=0)
    DST = DST[M]

    dictionary = concatenate([DCT,DST],axis=1)

    return dictionary


def omp(Y: ndarray, M: ndarray, n: int, n_coefs: int=None) -> ndarray:
    """
    Given Y of shape (len(M),n_targets), recover n_targets signals with joint sparsity of
    length len(M).
    Each signal - column of Y is the signal's observation on the support M

    Parameter
    ---------

    Y: ndarray (len(M),n_targets) matrix of the n_targets joint sparse signals
    M: index of the grid corresponding to the observations of the signals
    n: length of the grid on which the signal is undersampled
    n_coefs: passed to n_nonzero_coefs, a parameter of orthogonal_mp.
    If None set to 10% of n.

    Returns:
    Y_full: ndarray (n,n_targets) matrix of the recovered signals

    """

    dictionary = comp_dictionary(n,M)

    sparse_decomposition = orthogonal_mp(X=dictionary,y=Y,n_nonzero_coefs=n_coefs)

    dictionary = comp_dictionary(n,arange(n))

    Y_full = dictionary @ sparse_decomposition

    return Y_full













