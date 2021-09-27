import pytest
import numpy as np
from os.path import join

from SciDataTool import DataLinspace, DataTime
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
        normalizations={"ref": 2e-5},
        axes=[Angle, Time],
        values=field,
    )

    # Check slicing "time=sum"
    Field_extract = Field.get_data_along("angle", "time=sum")

    # Check transfer of normalizations
    assert Field.normalizations == Field_extract.normalizations


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
        normalizations={"ref": 2e-5},
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
        normalizations={"ref": 2e-5},
        axes=[Time, Angle],
        values=field.T,
    )

    Field_ft = Field.time_to_freq()

    Field_der = Field_ft.get_data_along("freqs=derivate")
    assert Field_der.unit == "m/s"
    Field_ft.unit = "m/s"
    Field_der = Field_ft.get_data_along("freqs=derivate")
    assert Field_der.unit == "m/s2"
    Field_ft.unit = "ms"
    Field_der = Field_ft.get_data_along("freqs=derivate")
    assert Field_der.unit == "m"
    Field_ft.unit = "ms2"
    Field_der = Field_ft.get_data_along("freqs=derivate")
    assert Field_der.unit == "ms"
    Field_ft.unit = "ms3"
    Field_der = Field_ft.get_data_along("freqs=derivate")
    assert Field_der.unit == "ms2"


if __name__ == "__main__":
    # test_get_data_along()
    # test_get_data_along_integrate()
    test_get_data_along_derivate()