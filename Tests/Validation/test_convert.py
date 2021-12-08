import pytest
from SciDataTool import (
    Data,
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
from SciDataTool.Functions import NormError
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
def test_units_fft():
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
    Field_ft = Field.time_to_freq()
    result = Field_ft.get_along("angle{°}")
    assert_array_almost_equal(180 / np.pi * angle, result["angle"])


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
        normalizations={"elec_order": Norm_ref(ref=50)},
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

    Time.symmetries["period"] = 2
    Time.normalizations["angle_rotor"] = Norm_vector(
        vector=np.linspace(0, 10, 20, endpoint=False)
    )
    # Normalization vector does not have the right size -> must raise error
    with pytest.raises(NormError):
        result = Field.get_along("time->angle_rotor")
    # With right size
    Time.normalizations["angle_rotor"] = Norm_vector(
        vector=np.linspace(0, 10, 10, endpoint=False)
    )
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
def test_setter_norm():
    """Check that you can set Normalization with the old format"""
    norm_dict = {
        "time": 20.5,
        "fe": 50,
        "rotor_angle": [0, 1, 2, 3],
        "rotor_angle2": np.array([0, 1, 2, 3]),
    }
    test_obj = Data(normalizations=norm_dict)

    assert len(test_obj.normalizations) == 4
    assert isinstance(test_obj.normalizations["time"], Norm_ref)
    assert test_obj.normalizations["time"].ref == 20.5

    assert isinstance(test_obj.normalizations["fe"], Norm_ref)
    assert test_obj.normalizations["fe"].ref == 50

    assert isinstance(test_obj.normalizations["rotor_angle"], Norm_vector)
    assert_array_almost_equal(
        test_obj.normalizations["rotor_angle"].vector, np.array([0, 1, 2, 3])
    )

    assert isinstance(test_obj.normalizations["rotor_angle2"], Norm_vector)
    assert_array_almost_equal(
        test_obj.normalizations["rotor_angle2"].vector, np.array([0, 1, 2, 3])
    )


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
        normalizations={"elec_order": Norm_ref(ref=5)},
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


@pytest.mark.validation
def test_dba_speed_order():
    Speed = DataLinspace(
        name="speed",
        unit="m/s",
        initial=0,
        final=10000,
        number=11,
        include_endpoint=True,
    )
    Order = Data1D(
        name="order",
        unit="",
        values=["H" + str(i) for i in range(20)],
    )
    Loadcase = DataLinspace(
        name="loadcases",
        unit="",
        initial=0,
        final=5,
        number=6,
        include_endpoint=True,
    )
    field = 600000 * np.ones((11, 20, 6))
    Field = DataFreq(
        name="noise",
        symbol="X",
        unit="Pa",
        values=field,
        axes=[Speed, Order, Loadcase],
        normalizations={"ref": Norm_ref(ref=2e-5)},
    )
    result = Field.get_magnitude_along("speed", "order", unit="dBA")
    assert result["X"].shape == (11, 20)
    result = Field.get_magnitude_along("speed", "order", "loadcases", unit="dBA")
    assert result["X"].shape == (11, 20, 6)


@pytest.mark.validation
def test_dba_speed_order_norm():
    Revolution = DataLinspace(
        name="revolution",
        unit="m/s",
        initial=0,
        final=10000,
        number=11,
        include_endpoint=True,
        normalizations={
            "time": Norm_ref(ref=2),
            "speed": Norm_vector(vector=np.linspace(0, 1000, 11)),
        },
    )
    Order = Data1D(
        name="order",
        unit="",
        values=["H" + str(i) for i in range(20)],
    )
    Loadcase = DataLinspace(
        name="loadcases",
        unit="",
        initial=0,
        final=5,
        number=6,
        include_endpoint=True,
    )
    field = 600000 * np.ones((11, 20, 6))
    Field = DataFreq(
        name="noise",
        symbol="X",
        unit="Pa",
        values=field,
        axes=[Revolution, Order, Loadcase],
        normalizations={"ref": Norm_ref(ref=2e-5)},
    )
    result = Field.get_magnitude_along("revolution->speed", "order", unit="dBA")
    assert result["X"].shape == (11, 20)
    result = Field.get_magnitude_along(
        "revolution->speed", "order", "loadcases", unit="dBA"
    )
    assert result["X"].shape == (11, 20, 6)


if __name__ == "__main__":
    test_dba_speed_order_norm()
    # test_norm()
    print("Done")