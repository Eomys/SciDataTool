from SciDataTool import DataLinspace, DataTime, Data1D
from numpy.random import random
from numpy import pi, zeros


f = 50
Nt_tot = 16
Na_tot = 20

Time = DataLinspace(name="time", unit="s", initial=0, final=1 / (2 * f), number=Nt_tot)
Angle = DataLinspace(name="angle", unit="rad", initial=0, final=2 * pi, number=Na_tot)
Z = DataLinspace(name="z", unit="m", initial=-1, final=1, number=3)

field = random((Nt_tot, Na_tot, 3))

Field = DataTime(
    name="Airgap flux density",
    symbol="B_r",
    unit="T",
    axes=[Time, Angle, Z],
    values=field,
)

X = DataLinspace(name="time", unit="s", initial=0, final=1, number=11)
Y = Data1D(
    name="loadcases",
    unit="",
    values=[
        "r=0, radial, stator",
        "r=-2, radial, stator",
        "r=2, radial, stator",
        "r=0, circumferential, stator",
        "r=-2, circumferential, stator",
        "r=2, circumferential, stator",
        "r=0, radial, rotor",
        "r=-2, radial, rotor",
        "r=2, radial, rotor",
        "r=0, circumferential, rotor",
        "r=-2, circumferential, rotor",
        "r=2, circumferential, rotor",
    ],
    is_components=True,
    delimiter=", ",
    filter={
        "wavenumber": ["r=0", "r=-2", "r=2"],
        "direction": ["radial", "circumferential"],
        "application": ["stator", "rotor"],
    },
    is_overlay=True,
)
field_filter = zeros((11, 12))
for i in range(12):
    field_filter[:, i] = i
Field_filter = DataTime(
    name="Airgap flux density",
    symbol="B_r",
    unit="T",
    axes=[X, Y],
    values=field_filter,
)
