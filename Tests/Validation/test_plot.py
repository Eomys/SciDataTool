import pytest
from SciDataTool import DataLinspace, DataTime, Data1D, Norm_affine
from Tests import save_validation_path
from SciDataTool.Functions.Plot.plot_2D import plot_2D
from numpy import meshgrid, pi, linspace, zeros, sin, split, sum
from os.path import join


@pytest.mark.validation
# @pytest.mark.DEV
def test_plot():
    """Test plot"""
    Time = DataLinspace(name="time", unit="s", initial=0, final=10, number=1001)
    Angle = DataLinspace(name="angle", unit="rad", initial=0, final=2 * pi, number=2001)
    angle, time = meshgrid(Angle.get_values(), Time.get_values())
    field = time + angle
    Field = DataTime(name="Example field", symbol="Z", axes=[Time, Angle], values=field)

    Field.plot_2D_Data(
        "time",
        "angle=[0,pi/4,pi/2]",
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_2D.png"),
    )
    Field.plot_3D_Data(
        "time",
        "angle{°}",
        is_2D_view=True,
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_3D.png"),
    )


def test_normalization():
    Time = DataLinspace(name="time", unit="s", initial=0, final=10, number=1001)
    time = Time.get_values()
    Time.normalizations = {"rpm": Norm_affine(slope=5, offset=2)}
    Angle = DataLinspace(name="angle", unit="rad", initial=0, final=2 * pi, number=2001)
    angle, time = meshgrid(Angle.get_values(), Time.get_values())
    field = time + angle
    Field = DataTime(name="Example field", symbol="Z", axes=[Time, Angle], values=field)

    Field.plot_2D_Data(
        "time->rpm",
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_norm.png"),
    )
    Field.plot_3D_Data(
        "time->rpm",
        "angle{°}",
        is_2D_view=True,
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_norm_3D.png"),
    )


def test_strings():
    Modes = Data1D(
        name="modes",
        unit="",
        values=["(0,0)", "(1,0)", "(2,0)", "(3,0)", "(4,0)"],
        is_components=True,
        is_overlay=False,
    )
    field = linspace(1, 5, 5)
    Field = DataTime(name="Example field", symbol="Z", axes=[Modes], values=field)

    Field.plot_2D_Data(
        "modes",
        type_plot="bargraph",
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_str.png"),
    )

    Freqs = DataLinspace(
        name="freqs",
        unit="Hz",
        initial=0,
        final=1000,
        number=11,
    )
    Modes.is_overlay = True
    field_2d = zeros((11, 5))
    for i in range(11):
        field_2d[i, :] = i * linspace(1, 5, 5)
    Field_2d = DataTime(
        name="Example field", symbol="Z", axes=[Freqs, Modes], values=field_2d
    )

    Field_2d.plot_2D_Data(
        "freqs",
        "modes",
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_str_2d.png"),
    )

    Field_2d.plot_3D_Data(
        "freqs",
        "modes",
        is_show_fig=False,
        save_path=join(save_validation_path, "plot_str_3d.png"),
    )


if __name__ == "__main__":
    test_plot()
    test_normalization()
    test_strings()
