from PySide2.QtWidgets import *
from SciDataTool.Classes.DataLinspace import DataLinspace
from SciDataTool.Classes.DataTime import DataTime
from SciDataTool.Classes.VectorField import VectorField
import numpy as np


if __name__ == "__main__":
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

    Field.plot()

    # Field.plot("time", "angle{°}", "z[2]", unit="T", zmax="50")
    # Field.plot("time", "angle[0]", "z[2]", unit="T", zmax="10")
    # Field.plot("wavenumber", "freqs", "z[2]", unit="T", zmax="50")
    # Field.plot("freqs", "wavenumber", "z=mean", unit="T", zmax="50")
    field_3d2 = np.zeros((11, 21, 3))
    for i in range(3):
        field_3d2[:, :, i] = (i + 2) * field

    Field2 = DataTime(
        name="Second component",
        symbol="B_r",
        unit="T",
        axes=[X, Y, Z],
        values=field_3d2,
    )
    Vecfield = VectorField(components={"comp_x": Field, "comp_y": Field2})
