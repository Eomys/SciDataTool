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
def test_two_comp():
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
    comp_y = DataTime(
        name="field",
        symbol="X_y",
        axes=[X, Y],
        values=field,
    )
    Field = VectorField(
        name="field", symbol="X_r", components={"comp_x": comp_x, "comp_y": comp_y}
    )
    result = Field.get_rphiz_along("x", "y")
    assert_array_almost_equal(
        np.array([1, np.sqrt(2), 1, 0, -1, -np.sqrt(2), -1, 0]), result["radial"][0, :]
    )
