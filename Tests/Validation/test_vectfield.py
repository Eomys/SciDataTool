import pytest
from SciDataTool import (
    DataTime,
    Data1D,
    DataLinspace,
    VectorField,
    Norm_ref,
    DataPattern,
)
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
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )
    Field_t = DataTime(
        name="Tangential field",
        symbol="X_t",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
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


@pytest.mark.validation
def test_xyz_rphiz():
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
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )
    Field_t = DataTime(
        name="Tangential field",
        symbol="X_t",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=-field.T,
    )
    VecField = VectorField(
        name="Example field",
        symbol="X",
        components={"radial": Field_r, "tangential": Field_t},
    )
    VecField_xyz = VecField.to_xyz()
    assert_array_almost_equal(
        VecField_xyz.components["comp_x"].values.T,
        field * np.cos(at) + field * np.sin(at),
    )
    assert_array_almost_equal(
        VecField_xyz.components["comp_y"].values.T,
        field * np.sin(at) - field * np.cos(at),
    )

    VecField_rphiz = VecField.to_rphiz()
    assert_array_almost_equal(
        VecField_rphiz.components["radial"].values.T,
        field,
    )
    assert_array_almost_equal(
        VecField_rphiz.components["tangential"].values.T,
        -field,
    )


@pytest.mark.validation
def test_xyz_sym():
    f = 50
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=10,
        include_endpoint=False,
        symmetries={"period": 5},
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi / 4,
        number=20,
        include_endpoint=False,
        symmetries={"antiperiod": 4},
    )
    Slice = DataPattern(
        name="z",
        unit="m",
        values=[-0.5],
        values_whole=[-0.5, 0.5],
        rebuild_indices=[0, 0],
    )
    field = np.zeros((10, 20, 1))
    at, ta = np.meshgrid(
        Angle.get_values(is_smallestperiod=True),
        Time.get_values(is_smallestperiod=True),
    )
    field[:, :, 0] = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    Field_r = DataTime(
        name="Radial field",
        symbol="X_r",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle, Slice],
        values=field,
    )
    VecField = VectorField(
        name="Example field",
        symbol="X",
        components={"radial": Field_r},
    )

    VecField_xyz = VecField.to_xyz()
    assert VecField_xyz.components["comp_x"].values.shape == (10, 20, 1)

    VecField_rphiz = VecField_xyz.to_rphiz()
    assert VecField_rphiz.compare(VecField) == [
        "len(selfcomponents)"
    ]  # Now contains tangential comp
    assert VecField_rphiz.components["radial"].compare(VecField.components["radial"])


@pytest.mark.validation
def test_get_vectorfield():
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
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )
    Field_t = DataTime(
        name="Tangential field",
        symbol="X_t",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=-field.T,
    )
    VecField = VectorField(
        name="Example field",
        symbol="X",
        components={"radial": Field_r, "tangential": Field_t},
    )
    VecField_sliced = VecField.get_vectorfield_along("time", "angle[0]")
    assert_array_almost_equal(
        VecField_sliced.components["radial"].values[:, 0],
        VecField.components["radial"].values[:, 0],
    )


if __name__ == "__main__":
    test_get_vectorfield()
