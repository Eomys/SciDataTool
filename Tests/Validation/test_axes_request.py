import pytest
import numpy as np
from os.path import join

from SciDataTool import DataLinspace, DataTime
from Tests import save_validation_path


@pytest.mark.validation
def test_request_sum():
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
        axes=[Angle, Time],
        values=field,
    )
    Field.plot_2D_Data(
        "angle",
        "time=sum",
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_2D_sum.png"),
    )


if __name__ == "__main__":
    test_request_sum()