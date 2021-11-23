from SciDataTool import DataLinspace, DataTime
from numpy.random import random
from numpy import pi


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
