import pytest
import numpy as np

from SciDataTool.Classes.Data1D import Data1D
from SciDataTool.Classes.DataTime import DataTime
from SciDataTool.Functions.omp import comp_undersampling, comp_undersampled_axe


@pytest.mark.validation
def test_omp_SMV():
    """
    Test the recovery of a sparse undersampled signal in the SMV (1D) situation
    """

    def f_1d(t: np.ndarray) -> np.ndarray:
        """
        Create a 1D function with the following Fourier transform coefficients:
        - 2 at 0 Hz
        - 4 at 12 Hz
        - 1 at 20 Hz
        """

        return (
            2
            + 3 * np.sin(5 * 2 * np.pi * t)
            + 4 * np.sin(12 * 2 * np.pi * t)
            + 1 * np.sin(20 * 2 * np.pi * t)
        )

    # Define a time vector
    n = 200
    time = np.linspace(0, 1, n, endpoint=False)
    Time = Data1D(name="time", unit="s", values=time)

    # Compute the signal the signal
    signal = f_1d(Time.values)
    Field = DataTime(
        name="field", symbol="X", axes=[Time], values=signal, unit="dimless"
    )

    # Randomly choose observations of the signal
    # Fix seed to avoid problem due to random non uniform sampling
    K = 0.3
    M, Time_under = comp_undersampling(K, Time, seed=90)

    # Undersample the signal
    signal_under = signal[M]

    # Create the DataTime undersampled object:
    Field_under = DataTime(
        name="field under",
        symbol="X",
        axes=[Time_under],
        values=signal_under,
        unit="dimless",
    )

    # Recover the signal with the OMP
    # The parameter n_coefs is the number of atoms of the dictionary used to recover the signal

    Field_recover = Field_under.orthogonal_mp(Time, n_coefs=10)
    signal_recover = Field_recover.values

    # Check that the result match the signal
    np.testing.assert_allclose(
        signal,
        signal_recover,
        rtol=1e-1,
        atol=1e-1,
    )


@pytest.mark.validation
def test_comp_undersampled_axe():
    """
    Test if comp_undersampled_axe is able to recover the observations - samples indices array M
    """

    n = 100
    time = np.linspace(0, 1, n, endpoint=False)

    Time = Data1D(
        name="time",
        unit="s",
        values=time,
    )

    # Randomly pick a percentage of the samples of the signal
    K = 0.5
    M, Time_under = comp_undersampling(K, Time, seed=10)

    np.testing.assert_array_equal(M, comp_undersampled_axe(Time, Time_under))


@pytest.mark.validation
def test_omp_dataND():
    """
    Test the recovery of a sparse undersampled signal in the MMV situation
    using the method DataND.orthogonal_mp
    """

    def f_2d(theta: np.ndarray, t: np.ndarray) -> np.ndarray:
        """
        Create a 2D function with the following Fourier transform coefficients:
        - 1 at 6 Hz
        - 3 at 10 Hz
        Wavenumber:
        - 20 {°}
        - 40 {°}
        """

        return (
            0
            + 2 * np.cos(6 * 2 * np.pi * t + 20 * theta / 360)
            + 1 * np.cos(10 * 2 * np.pi * t + 40 * theta / 360)
        )

    # Define the Time and Angle vector
    n = 200
    Time = Data1D(name="time", unit="s", values=np.linspace(0, 1, n, endpoint=False))
    Angle = Data1D(
        name="angle", unit="{°}", values=np.linspace(0, 40, 40, endpoint=False)
    )

    # Compute a grid of the space and the resulting field
    time_coord, angle_coord = np.meshgrid(Time.get_values(), Angle.get_values())
    field = f_2d(angle_coord, time_coord).T

    Field = DataTime(
        name="Field",
        symbol="X",
        unit="dimless",
        axes=[Time, Angle],
        values=field,
    )

    # Undersample the Time axis with 50% of the samples
    K = 0.2
    M, Time_under = comp_undersampling(K, Time, seed=8)

    # Compute a new grid and the resulting field
    time_under_coord, angle_under_coord = np.meshgrid(
        Time_under.get_values(), Angle.get_values()
    )
    field_under = f_2d(angle_under_coord, time_under_coord).T

    Field_under = DataTime(
        name="Field",
        symbol="X",
        unit="dimless",
        axes=[Time_under, Angle],
        values=field_under,
    )

    Field_recover = Field_under.orthogonal_mp(Time, n_coefs=8)

    field_recover = Field_recover.values

    # Check that the result match the true field
    np.testing.assert_allclose(
        field_recover,
        field,
        rtol=1e-1,
        atol=1e-1,
    )


@pytest.mark.validation
def test_comp_undersampling():
    """
    Test the undersampling function and that we can recover the undersampled indices
    """
    Time = Data1D(
        name="time",
        unit="s",
        values=np.linspace(0, 1, 100),
    )

    K = 0.5
    [M, Time_undersampled] = comp_undersampling(K, Time)

    assert len(M) == len(Time_undersampled.values)
    np.testing.assert_array_equal(M, comp_undersampled_axe(Time, Time_undersampled))

    K = 1.0
    [M, Time_undersampled] = comp_undersampling(K, Time)

    assert len(M) == len(Time_undersampled.values)
    np.testing.assert_array_equal(M, comp_undersampled_axe(Time, Time_undersampled))
