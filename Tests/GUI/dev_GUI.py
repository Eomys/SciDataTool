from PySide2.QtWidgets import *
from SciDataTool.Classes.DataLinspace import DataLinspace
from SciDataTool.Classes.DataTime import DataTime
from SciDataTool.Classes.VectorField import VectorField
from SciDataTool import Norm_ref
import numpy as np


if __name__ == "__main__":
    X = DataLinspace(name="time", unit="s", initial=0, final=10, number=11)
    Y = DataLinspace(name="angle", unit="rad", initial=0, final=2 * np.pi, number=21)
    Z = DataLinspace(name="z", unit="m", initial=-1, final=1, number=3, is_overlay=True)
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

    test = "plot"
    # test = "autoplot"
    # test = "plot_2axis"
    # test = "oneaxis"
    # test = "vect"
    # test = "is_overlay"

    if test == "plot":
        Field.plot()

    elif test == "plot_2axis":
        X = DataLinspace(name="time", unit="s", initial=0, final=10, number=11)
        Y = DataLinspace(
            name="angle", unit="rad", initial=0, final=2 * np.pi, number=21
        )
        y, x = np.meshgrid(Y.get_values(), X.get_values())
        field = x + y
        field_2d = np.zeros((11, 21))
        for i in range(21):
            field_2d[:, i] *= i + 1

        Field = DataTime(
            name="Airgap flux density",
            symbol="B_r",
            unit="T",
            axes=[X, Y],
            values=field_2d,
        )

        Field.plot("freqs", "angle[2]", unit="T", z_max=50)

    elif test == "autoplot":
        # Field.plot("angle{°}", "time", "z[2]", unit="T", z_max=50)
        Field.plot("time", "angle", "z[2]", frozen_type=1)
        # Field.plot("angle{°}", "z")
        # Field.plot("time", "angle[0]", "z[2]", unit="T", z_max=10)
        # Field.plot("wavenumber", "freqs", "z[2]", unit="T", z_max=50)
        # Field.plot("freqs", "wavenumber", "z=mean", unit="T", z_max=50)

    elif test == "is_overlay":
        Z = DataLinspace(
            name="z", unit="m", initial=-1, final=1, number=3, is_overlay=True
        )

        field_2d = np.ones((11, 3))
        for i in range(3):
            field_2d[:, i] *= i + 1

        Field = DataTime(
            name="Airgap flux density",
            symbol="B_r",
            unit="T",
            axes=[X, Z],
            values=field_2d,
        )

        Field.plot("time", "z[-1,0,1]")

    elif test == "oneaxis":

        field_1d = np.ones((11))
        for i in range(11):
            field_1d[i] *= i

        Field = DataTime(
            name="Airgap flux density",
            symbol="B_r",
            unit="T",
            axes=[X],
            values=field_1d,
        )

        Field.plot()

    elif test == "vect":

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
        VecField.plot()

        # VecField.plot("B[0]0", "time", "angle{°}", component="comp_x")
