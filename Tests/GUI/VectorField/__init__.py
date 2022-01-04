from SciDataTool import DataLinspace, DataTime, VectorField, Norm_ref
from numpy import pi, cos, meshgrid

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
    final=2 * pi,
    number=20,
    include_endpoint=False,
)

ta, at = meshgrid(Time.get_values(), Angle.get_values())
field = 5 * cos(2 * pi * f * ta + 3 * at)

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
