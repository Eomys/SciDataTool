import pytest
from SciDataTool import DataTime, Data1D, DataLinspace, DataPattern
import numpy as np
from numpy.testing import assert_array_almost_equal


@pytest.mark.validation
def test_period_linspace():
    time = np.linspace(0, 10, 10, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=10,
        number=10,
        include_endpoint=False,
    )
    Time_periodic = Time.get_axis_periodic(5)
    field = np.tile(np.arange(50, 60, 5), 5)
    field_periodic = np.arange(50, 60, 5)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
    )

    Time_bis = Time.get_axis_periodic(1, False)
    assert len(Time_bis.symmetries) == 0
    assert_array_almost_equal(Time.get_values(), Time_bis.get_values())

    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])

    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0, 2, 2, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0, 2, 2, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[0]")
    assert_array_almost_equal(0, result["time"])
    assert_array_almost_equal(50, result["X"])


@pytest.mark.validation
def test_period_1d():
    time = np.linspace(0, 10, 10, endpoint=False)
    Time = Data1D(
        name="time",
        unit="s",
        values=time,
    )
    Time_periodic = Time.get_axis_periodic(5)

    field = np.tile(np.arange(50, 60, 5), 5)
    field_periodic = np.arange(50, 60, 5)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
    )

    Time_bis = Time.get_axis_periodic(1, False)
    assert len(Time_bis.symmetries) == 0
    assert_array_almost_equal(Time.get_values(), Time_bis.get_values())

    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])

    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0, 2, 2, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0, 2, 2, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[0]")
    assert_array_almost_equal(0, result["time"])
    assert_array_almost_equal(50, result["X"])


@pytest.mark.validation
def test_antiperiod_linspace():
    time = np.linspace(0, 16, 16, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=16,
        number=16,
        include_endpoint=False,
    )
    Time_periodic = Time.get_axis_periodic(2, is_aper=True)
    field_periodic = np.arange(50, 70, 5)
    field_antisym = np.concatenate((field_periodic, np.negative(field_periodic)))
    field = np.tile(field_antisym, 2)

    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
    )
    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])

    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0, 4, 4, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[antiperiod]")
    assert_array_almost_equal(np.linspace(0, 4, 4, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0, 8, 8, endpoint=False), result["time"])
    assert_array_almost_equal(field_antisym, result["X"])

    result = Field.get_along("time[0]")
    assert_array_almost_equal(0, result["time"])
    assert_array_almost_equal(50, result["X"])


@pytest.mark.validation
def test_antiperiod_1d():
    time = np.linspace(0, 16, 16, endpoint=False)
    Time = Data1D(
        name="time",
        unit="s",
        values=time,
    )
    Time_periodic = Time.get_axis_periodic(2, is_aper=True)
    field_periodic = np.arange(50, 70, 5)
    field_antisym = np.concatenate((field_periodic, np.negative(field_periodic)))
    field = np.tile(field_antisym, 2)

    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
    )
    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])

    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0, 4, 4, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[antiperiod]")
    assert_array_almost_equal(np.linspace(0, 4, 4, endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])

    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0, 8, 8, endpoint=False), result["time"])
    assert_array_almost_equal(field_antisym, result["X"])

    result = Field.get_along("time[0]")
    assert_array_almost_equal(0, result["time"])
    assert_array_almost_equal(50, result["X"])


@pytest.mark.validation
def test_period_2d():
    time = np.linspace(0, 10, 10, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=10,
        number=10,
        include_endpoint=False,
    )
    Time_periodic = Time.get_axis_periodic(5)
    angle = np.linspace(0, 2 * np.pi, 16, endpoint=False)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=16,
        include_endpoint=False,
    )
    Angle_periodic = Angle.get_axis_periodic(2, is_aper=True)
    ta, at = np.meshgrid(
        Time_periodic.get_values(is_smallestperiod=True),
        Angle_periodic.get_values(is_smallestperiod=True),
    )
    field = np.cos(2 * np.pi * 50 * ta + at)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Angle_periodic, Time_periodic],
        values=field,
    )
    result = Field.get_along("time", "angle=[0,2*pi]")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(angle, result["angle"])


@pytest.mark.validation
def test_pattern():
    Slices = DataPattern(
        name="slice",
        unit="m",
        values=np.array([-5, -3, -1, 1, 3]),
        values_whole=np.array([-5, -3, -3, -1, -1, 1, 1, 3, 3, 5]),
        unique_indices=[0, 2, 4, 6, 8],
        rebuild_indices=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
    )
    field = np.array([10, 20, 30, 40, 50])
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Slices],
        values=field,
    )
    assert_array_almost_equal(10, Slices.get_length())
    assert_array_almost_equal(5, Slices.get_length(is_pattern=True))
    result = Field.get_along("slice")
    assert_array_almost_equal(
        np.array([-5, -3, -3, -1, -1, 1, 1, 3, 3, 5]), result["slice"]
    )
    assert_array_almost_equal(
        np.array([10, 10, 20, 20, 30, 30, 40, 40, 50, 50]), result["X"]
    )
    result = Field.get_along("slice[pattern]")
    assert_array_almost_equal(np.array([-5, -3, -1, 1, 3]), result["slice"])
    assert_array_almost_equal(field, result["X"])
    result = Field.get_along(
        "slice=axis_data",
        axis_data={"slice": np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])},
    )
    assert_array_almost_equal(
        np.array([10, 10, 15, 20, 25, 30, 35, 40, 45, 50, 50]), result["X"]
    )

    Slices = DataPattern(
        name="slice",
        unit="m",
        values=np.array([0]),
        unique_indices=[0],
        rebuild_indices=[0],
    )
    field = np.array([10])
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Slices],
        values=field,
    )
    result = Field.get_along(
        "slice=axis_data", axis_data={"slice": np.array([-2, -1, 0, 1, 2])}
    )
    assert_array_almost_equal(np.array([10, 10, 10, 10, 10]), result["X"])

    Slices = DataPattern(
        name="slice",
        unit="m",
        values=np.array([-5, -3, -1, 1, 3]),
        values_whole=np.array([-5, -3, -3, -1, -1, 1, 1, 3, 3, 5]),
        unique_indices=[0, 2, 4, 6, 8],
        rebuild_indices=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
    )
    field = np.array([10, 20, 30, 20, 10])
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Slices],
        values=field,
    )
    assert_array_almost_equal(10, Slices.get_length())
    assert_array_almost_equal(5, Slices.get_length(is_pattern=True))
    result = Field.get_along("slice")
    assert_array_almost_equal(
        np.array([-5, -3, -3, -1, -1, 1, 1, 3, 3, 5]), result["slice"]
    )
    assert_array_almost_equal(
        np.array([10, 10, 20, 20, 30, 30, 20, 20, 10, 10]), result["X"]
    )
    result = Field.get_along("slice[pattern]")
    assert_array_almost_equal(np.array([-5, -3, -1, 1, 3]), result["slice"])
    assert_array_almost_equal(field, result["X"])
    result = Field.get_along(
        "slice=axis_data",
        axis_data={"slice": np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])},
    )
    assert_array_almost_equal(
        np.array([10, 10, 15, 20, 25, 30, 25, 20, 15, 10, 10]), result["X"]
    )

    Slices = DataPattern(
        name="slice",
        unit="m",
        values=np.array([-5, -3, -1, 0]),
        values_whole=np.array([-5, -3, -3, -1, -1, 0, 1, 1, 3, 3, 5]),
        unique_indices=[0, 1, 3, 5],
        rebuild_indices=[0, 1, 1, 2, 2, 3, 2, 2, 1, 1, 0],
        is_step=False,
    )
    field = np.array([10, 20, 30, 35])
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Slices],
        values=field,
    )
    assert_array_almost_equal(11, Slices.get_length())
    assert_array_almost_equal(4, Slices.get_length(is_pattern=True))
    result = Field.get_along("slice")
    assert_array_almost_equal(
        np.array([-5, -3, -3, -1, -1, 0, 1, 1, 3, 3, 5]), result["slice"]
    )
    assert_array_almost_equal(
        np.array([10, 20, 20, 30, 30, 35, 30, 30, 20, 20, 10]), result["X"]
    )
    result = Field.get_along("slice[pattern]")
    assert_array_almost_equal(np.array([-5, -3, -1, 0]), result["slice"])
    assert_array_almost_equal(field, result["X"])
    result = Field.get_along(
        "slice=axis_data",
        axis_data={"slice": np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])},
    )
    assert_array_almost_equal(
        np.array([10, 15, 20, 25, 30, 35, 30, 25, 20, 15, 10]), result["X"]
    )


def test_period_single():
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=0,
        number=1,
        include_endpoint=False,
        symmetries={"antiperiod": 6, "delta": 3},
    )
    field = np.array([10])
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
    )
    result = Field.get_along("time")
    assert_array_almost_equal(np.array([0, 3, 6, 9, 12, 15]), result["time"])
    assert_array_almost_equal(np.array([10, -10, 10, -10, 10, -10]), result["X"])


if __name__ == "__main__":
    test_period_linspace()
    test_antiperiod_linspace()
    test_period_1d()
