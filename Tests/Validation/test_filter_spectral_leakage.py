import numpy as np
from numpy.testing import assert_array_almost_equal

import time as exec_time

from SciDataTool import DataLinspace, Data1D, DataTime, VectorField, DataFreq


is_show_fig = False


def test_filter_spectral_leakage_1d():
    """Test spectral leakage filter function with 1d field"""

    M = 200
    tf = 1
    Time = DataLinspace(
        name="time", unit="s", initial=0, final=tf, number=M, include_endpoint=False
    )
    time = Time.get_values()

    A0 = 2
    freq0 = 2.5
    phi0 = 0
    field = A0 * np.cos(2 * np.pi * freq0 * time + phi0)

    Field = DataTime(name="test field", symbol="X", axes=[Time], values=field)

    freqs_th = np.array([freq0])

    Field_filtered = Field.filter_spectral_leakage(freqs_th)

    result = Field_filtered.get_magnitude_along("freqs>0")

    assert_array_almost_equal(result["freqs"], freqs_th)
    assert_array_almost_equal(result["X"], 2)

    if is_show_fig:
        Field.plot_2D_Data(
            "freqs>0",
            data_list=[Field_filtered],
            legend_list=["Original", "Filtered"],
        )

    pass


def test_filter_spectral_leakage_2d():
    """Test spectral leakage filter function with 2d field"""

    M = 200
    tf = 1
    Time = DataLinspace(
        name="time", unit="s", initial=0, final=tf, number=M, include_endpoint=False
    )
    time = Time.get_values()
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=2016,
        include_endpoint=False,
    )
    angle = Angle.get_values()

    xangle, xtime = np.meshgrid(angle, time)

    A0 = 2
    freq0 = 2.5
    field = A0 * np.cos(2 * np.pi * freq0 * xtime + 3 * xangle)

    Field = DataTime(name="test field", symbol="X", axes=[Time, Angle], values=field)

    freqs_th = np.array([freq0])

    Field_filtered = Field.filter_spectral_leakage(freqs_th)

    result = Field_filtered.get_magnitude_along("freqs>0", "wavenumber")
    field_th = np.zeros(2016)
    field_th[1011] = 2

    assert_array_almost_equal(result["freqs"], freqs_th)
    assert_array_almost_equal(result["X"], field_th)

    if is_show_fig:
        Field.plot_3D_Data(
            "freqs>0",
            "wavenumber",
            is_2D_view=True,
            is_same_size=True,
        )
        Field_filtered.plot_3D_Data(
            "freqs>0",
            "wavenumber",
            is_2D_view=True,
            is_same_size=True,
        )

    pass


def test_filter_spectral_leakage_vectorfield():
    """Test spectral leakage filter method for vectorfield objects"""

    Nt = 512
    Na = 1024
    tf = 1
    Time = DataLinspace(
        name="time", unit="s", initial=0, final=tf, number=Nt, include_endpoint=False
    )
    time = Time.get_values()
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=Na,
        include_endpoint=False,
    )

    freqs_th = np.array([1, np.pi, 10, 20, 7 * np.pi])
    Freqs = Data1D(name="freqs", unit="Hz", values=freqs_th)

    wavenumber = np.array([-2, 0, 2])
    Wavenumber = Data1D(
        name="wavenumber",
        unit="",
        values=wavenumber,
    )

    FFT_r_val = np.zeros((freqs_th.size, wavenumber.size), dtype=complex)
    FFT_r_val[0, 0] = 1 + 1j
    FFT_r_val[1, 1] = 0.15 * np.exp(1j * np.pi / 8)
    FFT_r_val[2, 0] = 0.33 * np.exp(1j * 23 * np.pi / 12)
    FFT_r_val[3, 2] = 0.05
    FFT_r_val[4, 1] = -1j * 0.075

    FFT_t_val = np.zeros((freqs_th.size, wavenumber.size), dtype=complex)
    FFT_t_val[0, 0] = 0.333
    FFT_t_val[1, 1] = 0.5 - 0.2 * 1j
    FFT_t_val[2, 1] = 0.16 * np.exp(-1j * 23 * np.pi / 12)
    FFT_t_val[4, 0] = -0.05
    FFT_t_val[4, 2] = -1j * 0.075

    FFT_r = DataFreq(
        name="Radial quantity",
        symbol="X_r",
        unit="",
        values=FFT_r_val,
        axes=[Freqs, Wavenumber],
    )

    FFT_t = DataFreq(
        name="Tangential quantity",
        symbol="X_t",
        unit="",
        values=FFT_t_val,
        axes=[Freqs, Wavenumber],
    )

    FFT_vf = VectorField(
        name="Quantity", symbol="X", components={"radial": FFT_r, "tangential": FFT_t}
    )

    X_vf = FFT_vf.get_vectorfield_along(
        "time=axis_data",
        "angle=axis_data",
        axis_data={"time": time, "angle": Angle.get_values()},
    )

    start_time = exec_time.time()
    FFT_vf_filt = X_vf.filter_spectral_leakage(np.array(freqs_th))
    print(
        "Spectral leakage filter algorithm executed in: "
        + str(exec_time.time() - start_time)
        + " seconds"
    )

    start_time = exec_time.time()
    FFT_vf_nudft = X_vf.get_vectorfield_along(
        "freqs=axis_data", "wavenumber", axis_data={"freqs": freqs_th}
    )
    print(
        "NUDFT algorithm executed in: "
        + str(exec_time.time() - start_time)
        + " seconds"
    )

    # Compare values
    I0 = wavenumber + int(Na / 2)
    FFT_r_val_filt = FFT_vf_filt.components["radial"].values[:, I0]
    FFT_t_val_filt = FFT_vf_filt.components["tangential"].values[:, I0]
    assert_array_almost_equal(FFT_r_val - FFT_r_val_filt, 0, decimal=10)
    assert_array_almost_equal(FFT_t_val - FFT_t_val_filt, 0, decimal=10)

    if is_show_fig:
        X_vf.components["radial"].plot_3D_Data("time", "angle")
        X_vf.components["tangential"].plot_3D_Data("time", "angle")

        FFT_vf.components["radial"].plot_3D_Data("freqs", "wavenumber")
        X_vf.components["radial"].plot_3D_Data("freqs", "wavenumber")
        FFT_vf_filt.components["radial"].plot_3D_Data("freqs", "wavenumber")
        FFT_vf_nudft.components["radial"].plot_3D_Data("freqs", "wavenumber")

        FFT_vf.components["tangential"].plot_3D_Data("freqs", "wavenumber")
        X_vf.components["tangential"].plot_3D_Data("freqs", "wavenumber")
        FFT_vf_filt.components["tangential"].plot_3D_Data("freqs", "wavenumber")
        FFT_vf_nudft.components["tangential"].plot_3D_Data("freqs", "wavenumber")

    pass


if __name__ == "__main__":
    # test_filter_spectral_leakage_1d()
    # test_filter_spectral_leakage_2d()
    test_filter_spectral_leakage_vectorfield()
