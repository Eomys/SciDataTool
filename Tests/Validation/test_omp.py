# -*- coding: utf-8 -*-

import pytest
import numpy as np

from numpy import ndarray, sin, linspace, asarray, meshgrid, cos
from math import floor, pi

from SciDataTool.Classes.Data1D import Data1D
from SciDataTool.Classes.DataTime import DataTime
from SciDataTool.Classes.DataND import DataND
from SciDataTool.Functions.omp import comp_undersampling, omp, comp_undersampled_axe

@pytest.mark.validation
def test_omp_SMV():
    """
    Test the recovery of a sparse undersampled signal in the SMV situation
    """

    def f_1d(t: ndarray) -> ndarray:
        """
        Create a 1D function with the following Fourier transform coefficients:
        - 2 at 0 Hz
        - 3 at 5 Hz
        - 4 at 12 Hz
        - 1 at 20 Hz
        """

        return (
            2
            + 3 * sin(5 * 2 * pi * t)
            + 4 * sin(12 * 2 * pi * t)
            + 1 * sin(20 * 2 * pi * t)
        )

    # Define a time vector
    n = 1000
    time = linspace(0,1,n)
    Time = Data1D(name="time", unit="s", values=time)

    # Compute the signal the signal
    signal = f_1d(Time.values)
    field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=signal,
        unit="m"
    )

    # Randomly choose observations of the signal
    # Fix seed to avoid problem due to random non uniform sampling    
    K = 0.9
    M, Time_under = comp_undersampling(K, Time, seed=90)

    # Undersample the signal
    Y = signal[M]

    # Recover the signal with the OMP
    Y_full = omp(Y,M,n,n_coefs=8*2)

    # Check that the result match the signal
    np.testing.assert_allclose(
        Y_full,
        signal,
        rtol=1e-1,
        atol=1.5*1e-1,
    )


@pytest.mark.validation
def test_comp_undersampled_axe():
    """
    Test if comp_undersampled_axe is able to recover the observations - samples indices array M
    """

    n = 100
    time = linspace(0,1,n)

    Time = Data1D(
        name="time",
        unit="s",
        values=time,
    )

    # Randomly choose observations of the signal
    K = 0.5
    M, Time_under = comp_undersampling(K, Time, seed=10)

    np.testing.assert_array_equal(M,comp_undersampled_axe(Time,Time_under))


@pytest.mark.validation
def test_omp_dataND():
    """
    Test the recovery of a sparse undersampled signal in the MMV situation
    using the method DataND.orthogonal_mp
    """

    def f_2d(theta: ndarray, t: ndarray) -> ndarray:
        """
        Create a 2D function with the following Fourier transform coefficients:
        - 2 at 0 Hz
        - 1 at 4 Hz
        - 3 at 3 Hz
        Wavenumber:
        - 1 {°}
        - 3 {°}
        """

        return (
            2    
            + 1 * cos(4 * 2 * pi * t + 1 * theta)
            + 3 * cos(3 * 2 * pi * t + 3 * theta)
        )
    
    # Define the Time and Angle vector
    n = 100
    Time = Data1D(name="time", unit="s", values=linspace(0,1,n))
    Angle = Data1D(name="angle", unit="{°}", values=linspace(0,45,10))

    # Compute a grid of the space and the resulting field
    time_coord, angle_coord = meshgrid(Time.get_values(), Angle.get_values())
    field = f_2d(angle_coord, time_coord).T

    Field = DataTime(
        name="Field",
        symbol="X",
        unit="dimless",
        axes=[Time,Angle],
        values=field,
    )

    # Undersample the Time axis with 50% of the samples
    K = 0.90
    M, Time_under = comp_undersampling(K, Time, seed=65)

    # assert len(M) == len(Time.values)

    # Compute a new grid and the resulting field
    time_under_coord, angle_under_coord = meshgrid(Time_under.get_values(), Angle.get_values())
    field_under = f_2d(angle_under_coord,time_under_coord).T

    Field_under = DataTime(
        name="Field",
        symbol="X",
        unit="dimless",
        axes=[Time_under,Angle],
        values=field_under,
    )

    Field_recovered = Field_under.orthogonal_mp(Time, n_coefs=6)

    field_recovered = Field_recovered.values

    # Check that the result match the true field
    np.testing.assert_allclose(
        field_recovered,
        field,
        rtol=4*1e-1,
        atol=4*1e-1,
    )

@pytest.mark.validation
def test_comp_undersampling():
    """
    Test the undersampling function and that we can recover the undersampled indices
    """
    Time = Data1D(
        name="time",
        unit="s",
        values=linspace(0,1,100),
    )

    K = 0.5
    [M, Time_undersampled] = comp_undersampling(K,Time)

    assert len(M) == len(Time_undersampled.values)
    np.testing.assert_array_equal(M,comp_undersampled_axe(Time, Time_undersampled))

    K = 1.0
    [M, Time_undersampled] = comp_undersampling(K,Time)

    assert len(M) == len(Time_undersampled.values)
    np.testing.assert_array_equal(M,comp_undersampled_axe(Time, Time_undersampled))






