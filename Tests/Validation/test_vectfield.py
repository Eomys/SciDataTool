import pytest
from SciDataTool import DataTime, Data1D, DataLinspace, VectorField
import numpy as np
from numpy.testing import assert_array_almost_equal


@pytest.mark.validation
def test_one_comp():
    x = np.array(
        [
            6,
            6 * np.sqrt(2) / 2,
            0,
            -6 * np.sqrt(2) / 2,
            -6,
            -6 * np.sqrt(2) / 2,
            0,
            6 * np.sqrt(2) / 2,
        ]
    )
    y = np.array(
        [
            0,
            6 * np.sqrt(2) / 2,
            6,
            6 * np.sqrt(2) / 2,
            0,
            -6 * np.sqrt(2) / 2,
            -6,
            -6 * np.sqrt(2) / 2,
        ]
    )
    X = Data1D(
        name="x",
        unit="m",
        values=x,
    )
    Y = Data1D(
        name="y",
        unit="m",
        values=y,
    )
    field = np.ones((8, 8))
    comp_x = DataTime(
        name="field",
        symbol="X_x",
        axes=[X, Y],
        values=field,
    )
    Field = VectorField(name="field", symbol="X_r", components={"comp_x": comp_x})
    result = Field.get_xyz_along("x", "y")
    assert_array_almost_equal(field, result["comp_x"])
    assert_array_almost_equal(np.zeros((8, 8)), result["comp_y"])
    assert_array_almost_equal(np.zeros((8, 8)), result["comp_z"])


@pytest.mark.validation
def test_xyz_integration():
    f = 50
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
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
    ta, at = np.meshgrid(Time.get_values(), Angle.get_values())
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    Field_r = DataTime(
        name="Radial field",
        symbol="X_r",
        unit="m",
        normalizations={"ref": 2e-5},
        axes=[Time, Angle],
        values=field.T,
    )
    Field_t = DataTime(
        name="Tangential field",
        symbol="X_t",
        unit="m",
        normalizations={"ref": 2e-5},
        axes=[Time, Angle],
        values=-field.T,
    )
    VecField = VectorField(
        name="Example field",
        symbol="X",
        components={"radial": Field_r, "tangential": Field_t},
    )
    result = VecField.get_xyz_along("time", "angle=sum")
    assert result["comp_x"].shape == (10,)

    VecField_ft = VecField.time_to_freq()
    result = VecField_ft.get_xyz_along("time", "angle")
    assert result["comp_x"].shape == (10, 20)

    VecField_ft = VecField.time_to_freq()
    result = VecField_ft.get_xyz_along("time", "angle=sum")
    assert result["comp_x"].shape == (10,)


if __name__ == "__main__":
    test_xyz_integration()


# @pytest.mark.validation
# def test_two_comp():
#     x = np.array(
#         [
#             6,
#             6 * np.sqrt(2) / 2,
#             0,
#             -6 * np.sqrt(2) / 2,
#             -6,
#             -6 * np.sqrt(2) / 2,
#             0,
#             6 * np.sqrt(2) / 2,
#         ]
#     )
#     y = np.array(
#         [
#             0,
#             6 * np.sqrt(2) / 2,
#             6,
#             6 * np.sqrt(2) / 2,
#             0,
#             -6 * np.sqrt(2) / 2,
#             -6,
#             -6 * np.sqrt(2) / 2,
#         ]
#     )
#     X = Data1D(
#         name="x",
#         unit="m",
#         values=x,
#     )
#     Y = Data1D(
#         name="y",
#         unit="m",
#         values=y,
#     )
#     field = np.ones((8, 8))
#     comp_x = DataTime(
#         name="field",
#         symbol="X_x",
#         axes=[X, Y],
#         values=field,
#     )
#     comp_y = DataTime(
#         name="field",
#         symbol="X_y",
#         axes=[X, Y],
#         values=field,
#     )
#     Field = VectorField(
#         name="field", symbol="X_r", components={"comp_x": comp_x, "comp_y": comp_y}
#     )
#     result = Field.get_rphiz_along("x", "y")
#     assert_array_almost_equal(
#         np.array([1, np.sqrt(2), 1, 0, -1, -np.sqrt(2), -1, 0]), result["radial"][0, :]
#     )
