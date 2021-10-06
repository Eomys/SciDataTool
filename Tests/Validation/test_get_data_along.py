import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal
from os.path import join

from SciDataTool import DataLinspace, DataTime, Norm_ref
from SciDataTool.Functions import symmetries
from Tests import save_validation_path


@pytest.mark.validation
def test_get_data_along():
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
    Field = DataTime(
        name="Example field",
        symbol="X",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Angle, Time],
        values=field,
    )

    # Check slicing "time=sum"
    Field_extract = Field.get_data_along("angle", "time=sum")

    # Check transfer of normalizations
    assert Field.normalizations == Field_extract.normalizations
    assert isinstance(Field_extract.axes[0], DataLinspace)
    assert_array_almost_equal(
        Field_extract.axes[0].get_values(), Field.axes[0].get_values()
    )


@pytest.mark.validation
def test_get_data_along_symmetry():
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
        final=np.pi,
        number=20,
        include_endpoint=False,
        symmetries={"period": 2},
    )
    ta, at = np.meshgrid(Time.get_values(), Angle.get_values(is_smallestperiod=True))
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    Field = DataTime(
        name="Example field",
        symbol="X",
        normalizations={"ref": 2e-5},
        axes=[Angle, Time],
        values=field,
    )

    # Check slicing "time=sum"
    Field_extract = Field.get_data_along("angle", "time=sum")

    # Check transfer of symmetries
    assert Field_extract.axes[0].symmetries == dict()

    Field_extract = Field.get_data_along("angle[smallestperiod]", "time=sum")

    # Check transfer of symmetries
    assert Field_extract.axes[0].symmetries == {"period": 2}


@pytest.mark.validation
def test_get_data_along_single():
    f = 50
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=1,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=np.pi,
        number=20,
        include_endpoint=False,
        symmetries={"period": 2},
    )
    Slice = DataLinspace(
        name="z",
        unit="m",
        initial=0,
        final=10,
        number=30,
        include_endpoint=False,
    )
    ta, at = np.meshgrid(Time.get_values(), Angle.get_values(is_smallestperiod=True))
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    field_tot = np.zeros((1, 20, 30))
    for i in range(30):
        field_tot[:, :, i] = field.T + i
    Field = DataTime(
        name="Example field",
        symbol="X",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle, Slice],
        values=field_tot,
    )

    # Check slicing "z=sum"
    Field_extract = Field.get_data_along("time", "angle[smallestperiod]", "z=sum")

    # Check shape
    assert Field_extract.values.shape == (1, 20)
    # Check time axis
    assert Field_extract.axes[0].name == "time"


@pytest.mark.validation
def test_get_data_along_integrate():
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
    Field = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Angle, Time],
        values=field,
    )

    Field_int = Field.get_data_along("time=integrate", "angle")
    assert Field_int.unit == "ms"
    Field.unit = "ms"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "ms2"
    Field.unit = "m/s"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "m"
    Field.unit = "m/s2"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "m/s"
    Field.unit = "m/s3"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "m/s2"
    Field.unit = "ms"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "ms2"


@pytest.mark.validation
def test_get_data_along_derivate():
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
    Field = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )

    Field_ft = Field.time_to_freq()

    Field_der = Field_ft.get_data_along("freqs=derivate", "angle[0]")
    assert Field_der.unit == "m/s"
    result_ft = Field_ft.get_along("freqs", "angle[0]")
    freqs = result_ft["freqs"]
    field_ft = result_ft["X"]
    assert_array_almost_equal(Field_der.values, field_ft * 2 * 1j * np.pi * freqs)
    Field_ft.unit = "m/s"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "m/s2"
    Field_ft.unit = "ms"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "m"
    Field_ft.unit = "ms2"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "ms"
    Field_ft.unit = "ms3"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "ms2"


if __name__ == "__main__":
    test_get_data_along_single()
    # test_get_data_along_integrate()
    # test_get_data_along_derivate()