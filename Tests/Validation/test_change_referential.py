import numpy as np
from numpy.testing import assert_almost_equal

from SciDataTool import DataLinspace, DataTime, VectorField, DataPattern


is_show_fig = False

rotation_list = [-60, 60]


def test_change_referential_vf_waveform_per():
    """Test change_referential_waveform function with periodic vectorfield"""

    tf = 1
    k = 2
    r = 2
    rotation_speed = 60 * k / r
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=tf / k,
        number=200,
        include_endpoint=False,
        symmetries={"period": k},
    )
    time = Time.get_values(is_smallestperiod=True)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi / r,
        number=200,
        include_endpoint=False,
        symmetries={"period": r},
    )
    angle = Angle.get_values(is_smallestperiod=True)

    z = DataPattern(name="z", unit="m", values=np.array([0]))

    xangle, xtime = np.meshgrid(angle, time)

    A0 = 2
    field = A0 * np.cos(2 * np.pi * k * xtime + r * xangle) + 2 * A0 * np.cos(
        2 * np.pi * 2 * k * xtime + 2 * r * xangle
    )

    Field = VectorField(
        name="test field",
        components={
            "radial": DataTime(
                name="radial test field",
                symbol="X",
                unit="T",
                axes=[Time, Angle, z],
                values=field[:, :, None],
            ),
            "tangential": DataTime(
                name="tangential test field",
                symbol="X",
                unit="T",
                axes=[Time, Angle, z],
                values=field[:, :, None],
            ),
        },
    )

    # Change field to rotating referential
    Field_R = Field.change_referential(
        -rotation_speed, is_waveform=True, sym_t_new={"period": k}
    )

    # Change field back to static referential
    Field_RR = Field_R.change_referential(
        rotation_speed, is_waveform=True, sym_t_new={"period": k}
    )

    field_RR = Field_RR.get_rphiz_along(
        "time[smallestperiod]", "angle[smallestperiod]"
    )["radial"]

    assert_almost_equal(field, field_RR, decimal=7)

    if is_show_fig:

        Field.plot_2D_Data(
            "time[smallestperiod]",
            "angle[0]",
            data_list=[Field_RR],
            linestyles=["solid", "dotted"],
        )

        Field.plot_2D_Data(
            "angle[smallestperiod]",
            "time[0]",
            data_list=[Field_RR],
            linestyles=["solid", "dotted"],
        )

        Field.plot_3D_Data("time", "angle", is_same_size=True)

        Field_R.plot_3D_Data("time", "angle", is_same_size=True)

        Field_RR.plot_3D_Data("time", "angle", is_same_size=True)

        Field.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

        Field_R.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

        Field_RR.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

    pass


def test_change_referential_vf_waveform_aper():
    """Test change_referential_waveform function with antiperiodic vectorfield"""

    tf = 1
    k = 1
    r = 1
    rotation_speed = 60 * k / r
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=tf / (2 * k),
        number=200,
        include_endpoint=False,
        symmetries={"antiperiod": 2 * k},
    )
    time = Time.get_values(is_smallestperiod=True)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi / (2 * r),
        number=200,
        include_endpoint=False,
        symmetries={"antiperiod": 2 * r},
    )
    angle = Angle.get_values(is_smallestperiod=True)

    z = DataPattern(name="z", unit="m", values=np.array([0]))

    xangle, xtime = np.meshgrid(angle, time)

    A0 = 2
    field = A0 * np.cos(2 * np.pi * k * xtime + r * xangle) + 2 * A0 * np.cos(
        2 * np.pi * 3 * k * xtime + 3 * r * xangle
    )

    Field = VectorField(
        name="test field",
        components={
            "radial": DataTime(
                name="radial test field",
                symbol="X",
                unit="T",
                axes=[Time, Angle, z],
                values=field[:, :, None],
            ),
            "tangential": DataTime(
                name="tangential test field",
                symbol="X",
                unit="T",
                axes=[Time, Angle, z],
                values=field[:, :, None],
            ),
        },
    )

    # Change field to rotating referential
    Field_R = Field.change_referential(
        -rotation_speed, is_waveform=True, sym_t_new={"period": k}
    )

    # Change field back to static referential
    Field_RR = Field_R.change_referential(
        rotation_speed, is_waveform=True, sym_t_new={"antiperiod": 2 * k}
    )

    field_RR = Field_RR.get_rphiz_along(
        "time[smallestperiod]", "angle[smallestperiod]"
    )["radial"]

    assert_almost_equal(field, field_RR, decimal=5)

    if is_show_fig:

        Field.plot_2D_Data(
            "time[smallestperiod]",
            "angle[0]",
            data_list=[Field_RR],
            linestyles=["solid", "dotted"],
        )

        Field.plot_2D_Data(
            "angle[smallestperiod]",
            "time[0]",
            data_list=[Field_RR],
            linestyles=["solid", "dotted"],
        )

        Field.plot_3D_Data("time", "angle", is_same_size=True)

        Field_R.plot_3D_Data("time", "angle", is_same_size=True)

        Field_RR.plot_3D_Data("time", "angle", is_same_size=True)

        Field.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

        Field_R.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

        Field_RR.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

    pass


def test_change_referential_vf_spectrum():
    """Test change_referential_spectrum function with periodic vectorfield"""

    tf = 1
    k = 2
    r = 2
    rotation_speed = 60 * k / r
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=tf / k,
        number=100,
        include_endpoint=False,
        # symmetries={"antiperiod": 2 * k},
        symmetries={"period": k},
    )
    time = Time.get_values(is_smallestperiod=True)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi / r,
        number=20,
        include_endpoint=False,
        # symmetries={"antiperiod": 2 * r},
        symmetries={"period": r},
    )
    angle = Angle.get_values(is_smallestperiod=True)

    z = DataPattern(name="z", unit="m", values=np.array([0]))

    xangle, xtime = np.meshgrid(angle, time)

    A0 = 2
    field = A0 * np.cos(2 * np.pi * k * xtime + r * xangle) + 2 * A0 * np.cos(
        2 * np.pi * 2 * k * xtime + 2 * r * xangle
    )

    Field = VectorField(
        name="test field",
        components={
            "radial": DataTime(
                name="radial test field",
                symbol="X",
                unit="T",
                axes=[Time, Angle, z],
                values=field[:, :, None],
            )
        },
    )

    Field_R = Field.change_referential(-rotation_speed, is_waveform=False, atol=0)

    Field_RR = Field_R.change_referential(rotation_speed, is_waveform=False, atol=0)

    field_rk = Field.get_rphiz_along("freqs=" + str(k), "wavenumber=" + str(r))[
        "radial"
    ]

    field_R_rk = Field_R.get_rphiz_along("freqs=0", "wavenumber=" + str(r))["radial"]

    field_RR_rk = Field_RR.get_rphiz_along("freqs=" + str(k), "wavenumber=" + str(r))[
        "radial"
    ]
    assert_almost_equal(field_rk, 2 * field_R_rk)
    assert_almost_equal(field_rk, field_RR_rk)

    field_RR = Field_RR.get_rphiz_along("time", "angle")["radial"]
    assert_almost_equal(np.min(field), np.min(field_RR), decimal=3)
    assert_almost_equal(np.max(field), np.max(field_RR), decimal=3)
    assert_almost_equal(np.mean(field), np.mean(field_RR), decimal=3)

    if is_show_fig:
        Field.plot_3D_Data("time", "angle", is_same_size=True)

        Field_R.plot_3D_Data("time", "angle", is_same_size=True)

        Field_RR.plot_3D_Data("time", "angle", is_same_size=True)

        Field.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

        Field_R.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

        Field_RR.plot_3D_Data("freqs", "wavenumber", is_same_size=True)

    pass


if __name__ == "__main__":
    test_change_referential_vf_waveform_per()
    test_change_referential_vf_waveform_aper()
    test_change_referential_vf_spectrum()
