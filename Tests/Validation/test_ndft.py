import numpy as np
import random as rd
import pytest

from SciDataTool import Data1D, DataTime


@pytest.mark.validation
def test_nudft_1d():
    """
    Test DFT on non-uniform frequencies
    """

    def f_1d(x: np.ndarray) -> np.ndarray:
        """
        Create a 1D function with following Fourier transform coefficients:
        - 4 at 0 Hz
        - 20 at 4 Hz
        - 16 at 6 Hz
        - 10 at 20 Hz
        """
        return (
            4
            + 20 * np.sin(4 * 2 * np.pi * x)
            + 16 * np.sin(6 * 2 * np.pi * x)
            + 10 * np.sin(50 * 2 * np.pi * x)
        )

    # Define time discretization 200 samples
    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 200))

    # Define data
    data = f_1d(time.values)
    field = DataTime(
        name="field",
        symbol="X",
        axes=[time],
        values=data,
        unit="m",
    )

    # Compute non uniform discrete Fourier transform
    result_nudft = field.get_along(
        "freqs=axis_data", axis_data={"freqs": np.array([0, 4, 6, 50])}
    )

    # Create results dict to check nudft amplitude coefficient
    theoretical_amplitude_dict = {0: 4, 4: 20, 6: 16, 20: 10}

    # Check amplitudes
    for freq, val_fft in zip(result_nudft["freqs"], result_nudft["X"]):
        assert (
            np.abs(val_fft) == theoretical_amplitude_dict[freq]
        ), f"Non uniform dft amplitude is different from the theoretical one : {np.abs(val_fft)}!={theoretical_amplitude_dict[freq]}"


@pytest.mark.validation
def test_inudft_1d():
    """
    Test iDFT on non-uniform frequencies
    """

    def f_1d(x: np.ndarray) -> np.ndarray:
        """
        Create a 1D function with following Fourier transform coefficients:
        - 1 at 0 Hz
        - 5 at 2 Hz
        - 3 at 10 Hz
        - 8 at 13 Hz
        """
        return (
            1
            + 5 * np.sin(2 * 2 * np.pi * x)
            + 3 * np.sin(10 * 2 * np.pi * x)
            + 8 * np.sin(13 * 2 * np.pi * x)
        )

    # Define time discretization 200 samples
    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 200))

    # Define data
    data = f_1d(time.get_values())

    field = DataTime(
        name="field",
        symbol="X",
        axes=[time],
        values=data,
        unit="dimless",
    )

    # Compute non uniform discrete Fourier transform
    result_nudft = field.get_along(
        "freqs=axis_data", axis_data={"freqs": np.array([0, 2, 10, 13])}
    )

    # Define the spectral exis
    frequencies = Data1D(name="freqs", unit="Hz", values=result_nudft["freqs"])

    # Define the spectrum over the axis frequencies
    field = DataTime(
        name="field",
        symbol="X",
        axes=[frequencies],
        values=result_nudft["X"],
        unit="dimless",
    )

    result_inudft = field.get_along(
        "time=axis_data", axis_data={"time": np.linspace(0, 1, 200)}
    )

    np.testing.assert_array_almost_equal(result_inudft["X"], data)


@pytest.mark.validation
def test_force_nudft_1d():

    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 200))

    def f_1d(x):
        """
        Create a 1D function with following Fourier transform coefficients:
        - 2 at 0 Hz
        - 3 at 3 Hz
        - 4 at 9 Hz
        - 5 at 15 Hz
        """
        return (
            2
            + 3 * np.sin(3 * 2 * np.pi * x)
            + 4 * np.sin(9 * 2 * np.pi * x)
            + 5 * np.sin(15 * 2 * np.pi * x)
        )

    data = f_1d(time.get_values())

    field = DataTime(
        name="field",
        symbol="X",
        axes=[time],
        values=data,
        unit="dimless",
    )

    freqs = [i for i in range(200)]

    # Compute discrete Fourier transform
    result_fft = field.get_along(
        "freqs=axis_data", axis_data={"freqs": np.array(freqs)}
    )

    # the last element of freqs must trigger is_uniform test
    # epsilon = absolute(a - b) <= (atol + rtol * absolute(b))
    # the default parameters - (ndft_functions -> is_uniform) are rtol=1e-05, atol=1e-18

    freqs[-1] = freqs[-1] + 1e-8 + (1e-5 + 1e-6) * np.abs(freqs[-1])

    # Compute non uniform discrete Fourier transform
    result_nudft = field.get_along(
        "freqs=axis_data", axis_data={"freqs": np.array(freqs)}
    )

    assert np.allclose(
        result_fft["X"][:-1], result_nudft["X"][:-1]
    ), "The FFT and NUDFT methods sould return approximatly the same results"


@pytest.mark.validation
def test_nudft_2d():
    def f_2d(t, theta):
        """
        Create a 2D function with following Fourier transform coefficients:
        - 1 at 0 Hz
        - 2 at 15 Hz
        Wavenumber:
        - 3 at 10 {°}
        """

        return 1 + 3 * np.sin(10 * 2 * np.pi * theta) + 2 * np.sin(15 * 2 * np.pi * t)

    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 200))
    angle = Data1D(name="angle", unit="{°}", values=np.linspace(0, 360, 200))

    angle_coord, time_coord = np.meshgrid(time.get_values(), angle.get_values())

    field = f_2d(time_coord, angle_coord)

    Field = DataTime(
        name="Field", symbol="X", unit="dimless", axes=[time, angle], values=field
    )

    freqs_non_unif = np.linspace(0, 200, 400)
    freqs_non_unif = rd.sample(list(freqs_non_unif), 200)
    freqs_non_unif.sort()
    freqs_non_unif = np.asarray(freqs_non_unif)

    wavenumber_unif = [i for i in range(200)]

    # Compute non uniform discrete Fourier transform
    result_fft = field.get_along(
        "freqs=axis_data",
        "wavenumber=axis_data",
        axis_data={
            "freqs": np.array(freqs_non_unif),
            "wavenumber": np.array(wavenumber_unif),
        },
    )

    wavenumber = Data1D(name="wavenumber", unit="s", values=wavenumber)
    freqs = Data1D(name="freqs", unit="Hz", values=freqs_non_unif)

    angle_coord, time_coord = np.meshgrid(time.get_values(), angle.get_values())

    field = f_d(time_coord, angle_coord)

    Field = DataTime(
        name="Field", symbol="X", unit="dimless", axes=[time, angle], values=field
    )
