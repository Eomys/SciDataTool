import pytest

import numpy as np
from numpy.testing import assert_array_almost_equal

from SciDataTool import DataTime, DataFreq, Data1D, DataLinspace

arg_dict = {
    "is_auto_range": False,
    "is_auto_ticks": False,
    "x_min": -0.5,
    "x_max": 12,
    "y_min": -8,
    "y_max": 6,
}

val1 = {
    "f": np.array([0, 6, 2, 4]),
    "A": np.array(
        [1, -0.6 * 1j, -0.02 - 0.001 * 1j, 0.2 + 0.7 * 1j],
        dtype=complex,
    ),
}
val2 = {
    "f": np.array([0, 5]),
    "A": np.array([-1.5, np.sqrt(2) * 1j], dtype=complex),
}
val3 = {
    "f": np.array([1, 3, 7]),
    "A": np.array(
        [-0.1 * 0.3 * 1j, 0.0423 - 0.1 * 1j, -0.1 + 1.11 * 1j],
        dtype=complex,
    ),
}
val4 = {
    "f": np.array([2, 3, 6]),
    "A": np.array([1.2, np.sqrt(3) * 1j, np.exp(1j * np.pi / 11)], dtype=complex),
}

val_list = [
    {"f1": val1["f"], "f2": val1["f"], "A1": val1["A"], "A2": val1["A"]},
    {"f1": val1["f"], "f2": val2["f"], "A1": val1["A"], "A2": val2["A"]},
    {"f1": val1["f"], "f2": val3["f"], "A1": val1["A"], "A2": val3["A"]},
    {"f1": val1["f"], "f2": val4["f"], "A1": val1["A"], "A2": val4["A"]},
    {"f1": val2["f"], "f2": val2["f"], "A1": val2["A"], "A2": val2["A"]},
    {"f1": val2["f"], "f2": val3["f"], "A1": val2["A"], "A2": val3["A"]},
    {"f1": val2["f"], "f2": val4["f"], "A1": val2["A"], "A2": val4["A"]},
    {"f1": val3["f"], "f2": val3["f"], "A1": val3["A"], "A2": val3["A"]},
    {"f1": val3["f"], "f2": val4["f"], "A1": val3["A"], "A2": val4["A"]},
    {"f1": val4["f"], "f2": val4["f"], "A1": val4["A"], "A2": val4["A"]},
]

is_show_fig = False


@pytest.mark.parametrize("val_dict", val_list)
def test_conv(val_dict):
    """Test to validate convolution with direct comparaison to fft"""

    # Init first DataFreq
    Freqs1 = Data1D(name="freqs", unit="Hz", values=val_dict["f1"])

    df1 = DataFreq(
        name="Quantity 1", unit="", symbol="X1", values=val_dict["A1"], axes=[Freqs1]
    )

    # Init second spectrum
    Freqs2 = Data1D(name="freqs", unit="Hz", values=val_dict["f2"])
    df2 = DataFreq(
        name="Quantity 2", unit="", symbol="X2", values=val_dict["A2"], axes=[Freqs2]
    )

    # Convolve data1 and data2
    df3 = df1.conv(df2, name="Quantity 3 (df1.conv(df2))", symbol="X3", unit="")

    # Create DataTime from DataFreqs
    Nt = 512
    tf = 1
    Time = DataLinspace(
        name="time", unit="s", initial=0, final=tf, number=Nt, include_endpoint=False
    )
    time = Time.get_values()
    dt1 = df1.get_data_along("time=axis_data", axis_data={"time": time})
    dt2 = df2.get_data_along("time=axis_data", axis_data={"time": time})
    dt3 = DataTime(
        name="Quantity 3 (dt1*dt2)",
        unit="",
        symbol="X3",
        axes=dt1.get_axes(),
        values=dt1.values * dt2.values,
    )
    df3_bis = dt3.get_data_along("freqs")

    freqs_list = df3.axes[0].values.tolist()

    df3_bis_val = df3_bis.get_along("freqs=" + str(freqs_list))[df3_bis.symbol]

    assert_array_almost_equal(df3.values - df3_bis_val, 0, decimal=10)

    if is_show_fig:
        df3.plot_2D_Data("freqs", data_list=[df3_bis], legend_list=["conv", "FFT"])

    pass


@pytest.mark.parametrize("val_dict", val_list)
def test_sum(val_dict):
    """Test to validate convolution and to_Datatime method to rebuild signal in time / space domain"""

    # Init first DataFreq
    Freqs1 = Data1D(name="freqs", unit="Hz", values=val_dict["f1"])

    df1 = DataFreq(
        name="Quantity 1", unit="", symbol="X1", values=val_dict["A1"], axes=[Freqs1]
    )

    # Init second spectrum
    Freqs2 = Data1D(name="freqs", unit="Hz", values=val_dict["f2"])
    df2 = DataFreq(
        name="Quantity 2", unit="", symbol="X2", values=val_dict["A2"], axes=[Freqs2]
    )

    # Convolve data1 and data2
    df3 = df1.sum(df2, name="Quantity 3 (df1.sum(df2))", symbol="X3", unit="")

    # Create DataTime from DataFreqs
    Nt = 512
    tf = 1
    Time = DataLinspace(
        name="time", unit="s", initial=0, final=tf, number=Nt, include_endpoint=False
    )
    time = Time.get_values()
    dt1 = df1.get_data_along("time=axis_data", axis_data={"time": time})
    dt2 = df2.get_data_along("time=axis_data", axis_data={"time": time})
    dt3 = DataTime(
        name="Quantity 3 (dt1 + dt2)",
        unit="",
        symbol="X3",
        axes=dt1.get_axes(),
        values=dt1.values + dt2.values,
    )
    df3_bis = dt3.get_data_along("freqs")

    freqs_list = df3.axes[0].values.tolist()

    df3_bis_val = df3_bis.get_along("freqs=" + str(freqs_list))[df3_bis.symbol]

    if len(freqs_list) == 2:
        df3_bis_val = df3_bis_val[freqs_list]

    assert_array_almost_equal(df3.values - df3_bis_val, 0, decimal=10)

    if is_show_fig:
        df3.plot_2D_Data("freqs", data_list=[df3_bis], legend_list=["conv", "FFT"])

    pass


if __name__ == "__main__":

    for val_dict in val_list:
        test_conv(val_dict)

    for val_dict in val_list:
        test_sum(val_dict)

