import random as rd

import matplotlib.pyplot as plt
import numpy as np
import pytest
from SciDataTool import Data1D, DataTime, DataFreq


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
    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 10000))

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

    # Create results to check nudft amplitude coefficient
    theoretical_amplitude = np.array([4, 20, 16, 10], np.float64)

    # Check amplitudes
    np.testing.assert_array_almost_equal(
        np.abs(result_nudft["X"]), theoretical_amplitude, decimal=2
    )


@pytest.mark.validation
def test_inudft_1d():
    """
    Test iDFT on non-uniform frequencies, use nudft and inudft
    to compare with initial time series
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
            12.5
            - 30 * np.sin(2 * 2 * np.pi * x)
            + 40 * np.sin(10 * 2 * np.pi * x)
            + 18.9 * np.sin(13 * 2 * np.pi * x)
        )

    # Define time discretization 10000 samples
    time_vect = np.linspace(0, 1, 20_000)
    time = Data1D(name="time", unit="s", values=time_vect)

    # Define data
    data = f_1d(time.get_values())

    data_time = DataTime(
        name="field",
        symbol="X",
        axes=[time],
        values=data,
        unit="dimless",
    )

    # Compute non uniform discrete Fourier transform
    result_nudft = data_time.get_along(
        "freqs=axis_data", axis_data={"freqs": np.array([0, 2, 10, 13])}
    )

    # Define the spectral exis
    frequencies = Data1D(name="freqs", unit="Hz", values=result_nudft["freqs"])

    # Define the spectrum over the axis frequencies
    data_freq = DataFreq(
        name="field",
        symbol="X",
        axes=[frequencies],
        values=result_nudft["X"],
        unit="dimless",
    )

    # Compute inudftn
    result_inudft = data_freq.get_along("time=axis_data", axis_data={"time": time_vect})

    # Compare initial time serie with inudftn(nudftn) with a large tolerance
    np.testing.assert_array_almost_equal(
        result_inudft["X"].real, data_time.values, decimal=2
    )


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

    freqs = np.arange(200)

    # Compute discrete Fourier transform
    result_fft = field.get_along("freqs=axis_data", axis_data={"freqs": freqs})

    # the last element of freqs must trigger is_uniform test
    # epsilon = absolute(a - b) <= (atol + rtol * absolute(b))
    # the default parameters - (ndft_functions -> is_uniform) are rtol=1e-05, atol=1e-18

    freqs[-1] = freqs[-1] + 1e-8 + (1e-5 + 1e-6) * np.abs(freqs[-1])

    # Compute non uniform discrete Fourier transform
    result_nudft = field.get_along("freqs=axis_data", axis_data={"freqs": freqs})

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

    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 10_000))
    angle = Data1D(name="angle", unit="{°}", values=np.linspace(0, 360, 200))

    time_coord, angle_coord = np.meshgrid(time.get_values(), angle.get_values())

    field = f_2d(time_coord, angle_coord).T

    Field = DataTime(
        name="Field", symbol="X", unit="dimless", axes=[time, angle], values=field
    )

    freqs_non_unif = np.array([0, 15])

    # Compute non uniform discrete Fourier transform to get freqs and fft to get wavenumber
    result_dft = Field.get_along(
        "freqs=axis_data",
        "wavenumber",
        axis_data={
            "freqs": freqs_non_unif,
        },
    )

    assert result_dft["X"].shape == (
        len(freqs_non_unif),
        len(np.fft.fftfreq(len(angle.values))),
    )

    # Create DataFreq to test inudft
    wavenumber = Data1D(name="wavenumber", unit="s", values=result_dft["wavenumber"])
    freqs = Data1D(name="freqs", unit="Hz", values=result_dft["freqs"])

    FreqField = DataFreq(
        name="FreqField",
        symbol="X",
        unit="dimless",
        axes=[freqs, wavenumber],
        values=result_dft["X"],
    )

    result_idft = FreqField.get_along(
        "time=axis_data",
        "angle",
        axis_data={
            "time": time.values,
        },
    )

    np.testing.assert_array_almost_equal(result_idft["X"].real, field, decimal=3)


@pytest.mark.validation
def test_nudft_2d_wavenumber():
    def f_2d(t, theta):
        """
        Create a 2D function with following Fourier transform coefficients:
        - 1 at 0 Hz
        - 2 at 15 Hz
        Wavenumber:
        - 3 at 10 {rad^-1}
        """

        return 1 + 2 * np.sin(4 * 2 * np.pi * t) + 3 * np.sin(80 * theta)

    # Variable to display plot
    is_plot = False

    # Create DataTime
    time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 400))
    angle = Data1D(
        name="angle", unit="rad", values=np.linspace(0, 2 * np.pi, 300, endpoint=False)
    )

    time_coord, angle_coord = np.meshgrid(time.get_values(), angle.get_values())

    field = f_2d(time_coord, angle_coord).T

    Field = DataTime(
        name="Field",
        symbol="X",
        unit="dimless",
        axes=[time, angle],
        values=field,
    )
    if is_plot:  # Display field
        plt.imshow(field)
        plt.show()

    # Keep only interesting wavenumber
    wavenumber_non_unif = np.array([-80, 0, 80])

    # Compute non uniform dft along wavenumbers and fft along frequencies
    result_dft = Field.get_along(
        "freqs",
        "wavenumber=axis_data",
        axis_data={
            "wavenumber": wavenumber_non_unif,
        },
    )
    if is_plot:  # Display spectrum values
        plt.imshow(np.abs(result_dft["X"]))
        plt.show()

    # Check spectrum shape
    assert result_dft["X"].shape == (
        len(np.fft.rfftfreq(len(time.values))),
        len(wavenumber_non_unif),
    )

    # Create DataFreq to test inudft
    freqs = Data1D(name="freqs", unit="Hz", values=result_dft["freqs"])
    wavenumber = Data1D(name="wavenumber", unit="s", values=result_dft["wavenumber"])

    FreqField = DataFreq(
        name="FreqField",
        symbol="X",
        unit="dimless",
        axes=[freqs, wavenumber],
        values=result_dft["X"],
    )

    # Compute inverse non uniform DFT along wavenumbers and iFFT along frequencies
    result_idft = FreqField.get_along(
        "time",
        "angle=axis_data",
        axis_data={
            "angle": angle.values,
        },
    )

    if is_plot:  # Display field and reconstructed field to compare
        fig, axs = plt.subplots(2)
        axs[0].imshow(field)
        axs[1].imshow(
            result_idft["X"].real, vmin=0.9 * np.min(field), vmax=1.1 * np.nanmax(field)
        )
        plt.show()

    # Compare values between field and reconstructed field
    np.testing.assert_array_almost_equal(field, result_idft["X"].real)


def test_non_uniform_time_1d():
    """
    Perform inudft on a uniform spectrum to construct non uniform time serie
    """
    # Fix seed to avoid problem due to random non uniform sampling generation
    np.random.seed(5)

    def f_1d(x: np.ndarray) -> np.ndarray:
        """
        Create a 1D function with following Fourier transform coefficients:
        - 1 at 0 Hz
        - 5 at 2 Hz
        - 3 at 10 Hz
        - 8 at 13 Hz
        """
        return (
            12.5
            - 30 * np.sin(2 * 2 * np.pi * x)
            + 40 * np.sin(10 * 2 * np.pi * x)
            + 18.9 * np.sin(13 * 2 * np.pi * x)
        )

    # Define time discretization 200 samples
    time_vect = np.linspace(0, 1, 200)
    time = Data1D(name="time", unit="s", values=time_vect)

    # Define data
    data = f_1d(time.get_values())

    data_time = DataTime(
        name="field",
        symbol="X",
        axes=[time],
        values=data,
        unit="dimless",
    )

    # Compute non uniform discrete Fourier transform
    result_nudft = data_time.get_along("freqs")

    # Define the spectral exis
    frequencies = Data1D(name="freqs", unit="Hz", values=result_nudft["freqs"])

    # Define the spectrum over the axis frequencies
    data_freq = DataFreq(
        name="field",
        symbol="X",
        axes=[frequencies],
        values=result_nudft["X"],
        unit="dimless",
    )
    time_vect_non_unif = time_vect[::2] + np.random.normal(
        scale=1 / (10 * len(time_vect)), size=time_vect[::2].shape
    )

    # Compute inudftn
    result_inudft = data_freq.get_along(
        "time=axis_data", axis_data={"time": time_vect_non_unif}
    )

    # Compare initial time serie with inudftn(nudftn) with a large tolerance
    np.testing.assert_array_almost_equal(
        result_inudft["X"].real, f_1d(time_vect_non_unif), decimal=0
    )
    assert np.allclose(result_inudft["X"].real, f_1d(time_vect_non_unif), rtol=1e-1)


if __name__ == "__main__":
    test_nudft_2d()
