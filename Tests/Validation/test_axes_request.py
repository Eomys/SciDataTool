import pytest
import numpy as np
from os.path import join

from SciDataTool import DataLinspace, DataTime, Data1D
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


@pytest.mark.validation
def test_request_largest():
    X = DataLinspace(name="time", unit="s", initial=0, final=10, number=11)
    Y = Data1D(
        name="loadcases",
        unit="",
        values=[
            "r=0, radial, stator",  # 5
            "r=-2, radial, stator",  # 12
            "r=2, radial, stator",  # 6
            "r=0, circumferential, stator",  # 4
            "r=-2, circumferential, stator",  # 9
            "r=2, circumferential, stator",  # 2
            "r=0, radial, rotor",  # 11
            "r=-2, radial, rotor",  # 3
            "r=2, radial, rotor",  # 8
            "r=0, circumferential, rotor",  # 10
            "r=-2, circumferential, rotor",  # 1
            "r=2, circumferential, rotor",  # 7
        ],
        is_components=True,
        delimiter=", ",
        filter={
            "wavenumber": ["r=0", "r=-2", "r=2"],
            "direction": ["radial", "circumferential"],
            "application": ["stator", "rotor"],
        },
        sort_indices=[10, 5, 7, 3, 0, 2, 11, 8, 4, 9, 6, 1],
    )
    field = np.zeros((11, 12))
    Field = DataTime(
        name="Airgap flux density",
        symbol="B_r",
        unit="T",
        axes=[X, Y],
        values=field,
    )

    result = Field.get_along("time", "loadcases[5largest]")
    assert len(result["loadcases"]) == 5
    assert result["loadcases"].tolist() == [
        "r=-2, circumferential, rotor",
        "r=2, circumferential, stator",
        "r=-2, radial, rotor",
        "r=0, circumferential, stator",
        "r=0, radial, stator",
    ]
    assert result["B_r"].shape == (11, 5)


if __name__ == "__main__":
    # test_request_sum()
    test_request_largest()