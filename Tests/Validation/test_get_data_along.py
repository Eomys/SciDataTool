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


if __name__ == "__main__":
    test_get_data_along()