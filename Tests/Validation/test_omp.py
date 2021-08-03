import matplotlib.pyplot as plt
import numpy as np
import pytest

from math import floor
from SciDataTool import Data1D, DataTime, DataFreq, DataND

from SciDataTool.Functions.omp import omp

@pytest.mark.validation
def test_omp_SMV():
    """
    Test the recovery of a sparse undersampled signal in the SMV situation
    """

    def f_1d(x: np.ndarray) -> np.ndarray:
        """
        Create a 1D function with the following Fourier transform coefficients:
        - 2 at 0 Hz
        - 3 at 5 Hz
        - 4 at 12 Hz
        - 1 at 20 Hz
        """

        return (
            2
            + 3 * np.sin(5 * 2 * np.pi * x)
            + 4 * np.sin(12 * 2 * np.pi * x)
            + 1 * np.sin(20 * 2 * np.pi * x)
        )

    # Define a time vector
    n = 1000
    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, n))

    # Compute the signal the signal
    signal = f_1d(time.values)
    field = DataTime(
        name="field",
        symbol="X",
        axes=[time],
        values=signal,
        unit="m"
    )

    # fix seed to avoid problem due to random non uniform sampling
    np.random.seed(90)

    # Randomly choose observations of the signal
    # a subset M of the time-grid
    K = 0.90
    m = floor(K*n)
    M = np.random.choice(n,m, replace=False)
    M.sort()
    M = np.asarray(M)

    # Undersample the signal
    Y = signal[M]

    # recover the signal with the OMP
    Y_full = omp(Y,M,n,n_coefs=8*2)

    # Check that the result match the signal
    np.testing.assert_allclose(
        Y_full,
        signal,
        rtol=1e-1,
        atol=1.5*1e-1,
    )











