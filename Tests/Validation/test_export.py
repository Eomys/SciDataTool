import pytest
from SciDataTool import DataTime, DataLinspace
from Tests import save_validation_path
import numpy as np


@pytest.mark.validation
def test_export_2D():
    """Test export"""
    X = DataLinspace(name="time", unit="s", initial=0, final=10, number=11)
    Y = DataLinspace(name="angle", unit="rad", initial=0, final=2 * np.pi, number=21)
    y, x = np.meshgrid(Y.get_values(), X.get_values())
    field = x + y
    Field = DataTime(
        name="Airgap flux density", symbol="B_r", unit="T", axes=[X, Y], values=field
    )

    Field.export_along("time", "angle{°}", save_path=save_validation_path)
    Field.export_along(
        "time=1",
        "angle{°}",
        save_path=save_validation_path,
        file_name="B_r_Data_sliced",
    )


def test_export_3D():
    """Test export"""
    X = DataLinspace(name="time", unit="s", initial=0, final=10, number=11)
    Y = DataLinspace(name="angle", unit="rad", initial=0, final=2 * np.pi, number=21)
    Z = DataLinspace(name="z", unit="m", initial=-1, final=1, number=3)
    y, x = np.meshgrid(Y.get_values(), X.get_values())
    field = x + y
    field_3d = np.zeros((11, 21, 3))
    for i in range(3):
        field_3d[:, :, i] = (i + 1) * field
    Field = DataTime(
        name="Airgap flux density",
        symbol="B_r",
        unit="T",
        axes=[X, Y, Z],
        values=field_3d,
    )

    Field.export_along(
        "time=1",
        "angle{°}",
        save_path=save_validation_path,
        file_name="B_r_Data_sliced",
    )
    Field.export_along(
        "time", "angle{°}", "z", save_path=save_validation_path, is_multiple_files=True
    )
    Field.export_along(
        save_path=save_validation_path,
        is_multiple_files=True,
        file_name="B_r_withoutargs",
    )


if __name__ == "__main__":
    # test_export_2D()
    test_export_3D()
