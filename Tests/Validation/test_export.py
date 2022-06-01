import pytest
from SciDataTool import DataTime, DataLinspace, Data1D
from Tests import save_validation_path
import numpy as np
from os.path import isfile, join


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
    assert isfile(join(save_validation_path, "B_r_Data.csv"))
    Field.export_along(
        "angle{°}",
        "time=1",
        save_path=save_validation_path,
        file_name="B_r_Data_sliced",
    )
    assert isfile(join(save_validation_path, "B_r_Data_sliced.csv"))


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
        "angle{°}",
        "time=1",
        save_path=save_validation_path,
        file_name="B_r_Data3D_sliced",
    )
    assert isfile(join(save_validation_path, "B_r_Data3D_sliced.csv"))
    Field.export_along(
        "time",
        "angle{°}",
        "z",
        save_path=save_validation_path,
        is_multiple_files=True,
        is_2D=False,
    )
    assert isfile(join(save_validation_path, "B_r_Data_z0.0.csv"))
    assert isfile(join(save_validation_path, "B_r_Data_z1.0.csv"))
    assert isfile(join(save_validation_path, "B_r_Data_z-1.0.csv"))
    Field.export_along(
        save_path=save_validation_path,
        is_multiple_files=True,
        file_name="B_r_withoutargs",
        is_2D=False,
    )
    assert isfile(join(save_validation_path, "B_r_withoutargs_z0.0.csv"))
    assert isfile(join(save_validation_path, "B_r_withoutargs_z1.0.csv"))
    assert isfile(join(save_validation_path, "B_r_withoutargs_z-1.0.csv"))


def test_export_latex():
    """Test export"""
    X = DataLinspace(name="time", unit="s", initial=0, final=10, number=11)
    Y = Data1D(
        name="order",
        unit="",
        values=["H24 ($3f_{e}$)", "H48 ($6f_{e}$)"],
        is_components=True,
    )
    field = np.zeros((11, 2))
    Field = DataTime(
        name="Airgap flux density",
        symbol="B_r",
        unit="T",
        axes=[X, Y],
        values=field,
    )
    Field.export_along(
        "time",
        "order",
        save_path=save_validation_path,
        file_name="B_r_Data3D_latex",
    )


if __name__ == "__main__":
    test_export_2D()
    test_export_3D()
    test_export_latex()
