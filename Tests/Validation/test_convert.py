import pytest
from SciDataTool import (
    DataTime,
    DataLinspace,
    Data1D,
    DataFreq,
    Norm_affine,
    Norm_func,
    Norm_indices,
    Norm_vector,
    Norm_ref,
)
from Tests import DATA_DIR
import numpy as np
from numpy.testing import assert_array_almost_equal
from os.path import join
import matplotlib.pyplot as plt


@pytest.mark.validation
def test_units():
    time = np.linspace(0, 10, 10, endpoint=False)
    angle = np.linspace(0, 2 * np.pi, 20, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=10,
        number=10,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=20,
        include_endpoint=False,
    )
    field = np.ones((10, 20))
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m/s2",
    )
    result = Field.get_along("time{ms}", unit="km/h2")
    assert_array_almost_equal(1e3 * time, result["time"])
    assert_array_almost_equal(12960 * field[:, 0], result["X"])

    result = Field.get_along("angle{°}", unit="dm/ms2")
    assert_array_almost_equal(180 / np.pi * angle, result["angle"])
    assert_array_almost_equal(1e-5 * field[0, :], result["X"])


@pytest.mark.validation
def test_norm():
    f = 50
    time = np.linspace(0, 1 / f, 10, endpoint=False)

    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=10,
        include_endpoint=False,
        normalizations={"elec_order": Norm_affine(slope=50)},
    )
    field = np.cos(2 * np.pi * 2 * f * time)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
        unit="m/s2",
        normalizations={"ref": Norm_ref(ref=0.2)},
    )
    result = Field.get_along("freqs->elec_order=[0,3]", is_norm=True)
    assert_array_almost_equal(np.linspace(0, 3, 4), result["freqs"])
    assert_array_almost_equal(1 / 0.2, result["X"][2])

    Time.normalizations["angle_rotor"] = Norm_func(function=lambda x: 50 * x + 2)
    result = Field.get_along("time->angle_rotor")
    assert_array_almost_equal(50 * time + 2, result["time"])

    Time.normalizations["angle_rotor"] = Norm_vector(
        vector=np.linspace(0, 10, 10, endpoint=False)
    )
    Time.symmetries["period"] = 2
    result = Field.get_along("time->angle_rotor")
    assert_array_almost_equal(np.linspace(0, 20, 20, endpoint=False), result["time"])
    result = Field.get_along("time->angle_rotor[smallestperiod]")
    assert_array_almost_equal(np.linspace(0, 10, 10, endpoint=False), result["time"])

    angle = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=10,
        include_endpoint=False,
        normalizations={"tooth_id": Norm_indices()},
    )
    field = np.cos(2 * np.pi * 100 * angle)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Angle],
        values=field,
        unit="m/s2",
    )
    result = Field.get_along("angle->tooth_id")
    assert_array_almost_equal(np.linspace(0, 10, 10, endpoint=False), result["angle"])


@pytest.mark.validation
def test_noct():
    data = np.load(join(DATA_DIR, "pinknoise_fine_band.npy"))
    freqs = data[1, :]
    field = data[0, :]
    data_oct = np.load(join(DATA_DIR, "pinknoise_third_oct.npy"))
    foct = data_oct[1, :]
    field_oct = data_oct[0, :]

    Freqs = Data1D(name="freqs", unit="Hz", values=freqs)
    Field = DataFreq(
        name="pink noise",
        symbol="X",
        unit="Pa",
        values=field,
        axes=[Freqs],
        normalizations={"ref": Norm_ref(ref=2e-5)},
    )
    F_oct = Data1D(name="freqs", unit="Hz", values=foct)
    Field_oct = DataFreq(
        name="pink noise",
        symbol="X",
        unit="Pa",
        values=field_oct,
        axes=[F_oct],
        normalizations={"ref": Norm_ref(ref=2e-5)},
    )

    Field.plot_2D_Data("freqs=[24,20000]->1/3oct", unit="dB")
    fig = plt.gcf()
    ax = plt.gca()
    Field_oct.plot_2D_Data(
        "freqs",
        unit="dB",
        fig=fig,
        ax=ax,
        legend_list=["SciDataTool", "Reference"],
        color_list=["tab:red"],
    )


@pytest.mark.validation
def test_dba():
    data = np.load(join(DATA_DIR, "pinknoise_fine_band.npy"))
    freqs = data[1, :]
    field = data[0, :]

    Freqs = Data1D(
        name="freqs",
        unit="Hz",
        values=freqs,
        normalizations={"elec_order": Norm_affine(slope=5)},
    )
    Field = DataFreq(
        name="pink noise",
        symbol="X",
        unit="Pa",
        values=field,
        axes=[Freqs],
        normalizations={"ref": Norm_ref(ref=2e-5)},
    )
    result_Hz = Field.get_along("freqs", unit="dBA")
    result_elec_order = Field.get_along("freqs->elec_order", unit="dBA")
    assert_array_almost_equal(result_Hz["X"], result_elec_order["X"])

    result_Hz = Field.get_magnitude_along("freqs", unit="dBA")
    result_elec_order = Field.get_magnitude_along("freqs->elec_order", unit="dBA")
    assert_array_almost_equal(result_Hz["X"], result_elec_order["X"])


if __name__ == "__main__":
    test_norm()
