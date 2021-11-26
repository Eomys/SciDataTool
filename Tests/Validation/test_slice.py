import pytest
from SciDataTool import DataLinspace, DataTime, DataPattern
from numpy import meshgrid, linspace, array, repeat, nan, trapz, pi, cos
from numpy.testing import assert_array_almost_equal


@pytest.mark.validation
# @pytest.mark.DEV
def test_slice():
    """Test slicing"""
    X = DataLinspace(name="time", unit="m", initial=0, final=10, number=11)
    Y = DataLinspace(name="Y", unit="m", initial=0, final=100, number=11)
    y, x = meshgrid(Y.get_values(), X.get_values())
    field = x + y
    Field = DataTime(name="Example field", symbol="Z", axes=[X, Y], values=field)

    # Extract data by axis value
    # 'X=1'
    # result = Field.get_along("X=1", "Y")
    # assert_array_almost_equal(field[1, :], result["Z"])

    # 'X=20' (out of bounds)
    result = Field.get_along("time=20", "Y")
    assert_array_almost_equal(repeat(nan, 11), result["Z"])

    # 'X=[0, 1]'
    result = Field.get_along("time=[0, 1]", "Y")
    expected = field[0:2, :]
    assert_array_almost_equal(expected, result["Z"])

    # 'X<2' #TODO result in an error
    result = Field.get_along("time<2", "Y")
    expected = field[0:2, :]
    # assert_array_almost_equal(expected, result["Z"])

    # Extract data by operator
    # mean value 'Y=mean' (arithmetic)
    result = Field.get_along("time", "Y=mean")
    expected = (field).mean(axis=1)
    assert_array_almost_equal(expected, result["Z"])

    # sum 'X=sum'
    result = Field.get_along("time=sum", "Y")
    expected = field.sum(axis=0)
    assert_array_almost_equal(expected, result["Z"])

    # rms value 'Y=rms' (arithmetic)
    result = Field.get_along("time", "Y=rms")
    expected = (field ** 2).mean(axis=1) ** (1 / 2)
    assert_array_almost_equal(expected, result["Z"])

    # Extract data by indices
    result = Field.get_along("time[1:5]", "Y[2:8]")
    expected = field[1:5, 2:8]
    assert_array_almost_equal(expected, result["Z"])

    # Step axis
    X = DataPattern(
        name="time",
        unit="m",
        values=array([-0.5, -0.3, -0.1, 0.1, 0.3]),
        values_whole=array([-0.5, -0.3, -0.3, -0.1, -0.1, 0.1, 0.1, 0.3, 0.3, 0.5]),
        rebuild_indices=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
    )
    field = array([20, 40, 60, 80, 100])
    y, field_x = meshgrid(Y.get_values(), field)
    field = field_x + y
    Field = DataTime(name="Example field", symbol="Z", axes=[X, Y], values=field)
    result = Field.get_along("time=integrate", "Y")
    expected = 300 * 0.2 + linspace(0, 100, 11)
    assert_array_almost_equal(expected, result["Z"])

    # Interpolation on double point
    f = 50
    Nt_tot = 10
    Na_tot = 2 ** 11
    time = linspace(0, 1 / f, Nt_tot, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=Nt_tot,
        include_endpoint=False,
    )

    angle = linspace(0, 2 * pi, Na_tot, endpoint=False)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * pi,
        number=Na_tot,
        include_endpoint=False,
    )
    zlong = array([-1, 1])
    Slice = DataPattern(
        name="z",
        unit="m",
        values=[-1, 0],
        is_step=True,
        values_whole=[-1, 0, 0, 1],
        rebuild_indices=[0, 0, 1, 1],
    )
    at, ta, zat = meshgrid(angle, time, zlong)
    field = 2e5 * cos(2 * pi * 2 * f * ta + 2 * at)
    Field = DataTime(
        name="Radial AGSF",
        unit="N/m^2",
        symbol="AGSF_r",
        axes=[Time, Angle, Slice],
        values=field[:, None],
    )
    result = Field.get_along(
        "time", "angle", "z=axis_data", axis_data={"z": array([0.0])}
    )
    assert result["AGSF_r"].shape == (10, 2048)
    result = Field.get_along(
        "time", "angle", "z=axis_data", axis_data={"z": array([-1.0, 0.0, 1.0])}
    )
    assert result["AGSF_r"].shape == (10, 2048, 3)


if __name__ == "__main__":
    test_slice()
