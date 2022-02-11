import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_equal

from SciDataTool import DataLinspace, DataTime, Norm_ref, Data1D, DataPattern


@pytest.mark.validation
def test_get_data_along():
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
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Angle, Time],
        values=field,
    )

    # Check slicing "time=sum"
    Field_extract = Field.get_data_along("angle", "time=sum")

    # Check transfer of normalizations
    assert Field.normalizations == Field_extract.normalizations
    assert isinstance(Field_extract.axes[0], DataLinspace)
    assert_array_almost_equal(
        Field_extract.axes[0].get_values(), Field.axes[0].get_values()
    )


@pytest.mark.validation
def test_get_data_along_symmetry():
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
        final=np.pi,
        number=20,
        include_endpoint=False,
        symmetries={"period": 2},
    )
    ta, at = np.meshgrid(Time.get_values(), Angle.get_values(is_smallestperiod=True))
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    Field = DataTime(
        name="Example field",
        symbol="X",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Angle, Time],
        values=field,
    )

    # Check slicing "time=sum"
    Field_extract = Field.get_data_along("angle", "time=sum")

    # Check transfer of symmetries
    assert Field_extract.axes[0].symmetries == dict()

    Field_extract = Field.get_data_along("angle[smallestperiod]", "time=sum")

    # Check transfer of symmetries
    assert Field_extract.axes[0].symmetries == {"period": 2}


@pytest.mark.validation
def test_get_data_along_single():
    f = 50
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=1,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=np.pi,
        number=20,
        include_endpoint=False,
        symmetries={"period": 2},
    )
    Slice = DataLinspace(
        name="z",
        unit="m",
        initial=0,
        final=10,
        number=30,
        include_endpoint=False,
    )
    ta, at = np.meshgrid(Time.get_values(), Angle.get_values(is_smallestperiod=True))
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    field_tot = np.zeros((1, 20, 30))
    for i in range(30):
        field_tot[:, :, i] = field.T + i
    Field = DataTime(
        name="Example field",
        symbol="X",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle, Slice],
        values=field_tot,
    )

    # Check slicing "z=sum"
    Field_extract = Field.get_data_along("time", "angle[smallestperiod]", "z=sum")

    # Check shape
    assert Field_extract.values.shape == (1, 20)
    # Check time axis
    assert Field_extract.axes[0].name == "time"


@pytest.mark.validation
def test_get_data_along_integrate():

    # Test integrate / sum / mean / rms with and without anti-periodicity
    f = 50
    A = 5
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
    field = A * np.cos(2 * np.pi * f * ta + 3 * at)
    Field = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )

    Field_int = Field.get_data_along("time=integrate", "angle")
    assert_array_almost_equal(Field_int.values, 0, decimal=16)
    assert Field_int.unit == "ms"
    Field_mean = Field.get_data_along("time=mean", "angle")
    assert_array_almost_equal(Field_mean.values, 0, decimal=15)
    assert Field_mean.unit == "m"
    Field_sum = Field.get_data_along("time=sum", "angle")
    assert_array_almost_equal(Field_sum.values, 0, decimal=14)
    assert Field_sum.unit == "m"
    Field_rms = Field.get_data_along("time=rms", "angle")
    assert_array_almost_equal(Field_rms.values, A / np.sqrt(2), decimal=15)
    assert Field_rms.unit == "m"
    Field_int_loc = Field.get_data_along("time=integrate_local", "angle")
    assert_array_almost_equal(np.sum(Field_int_loc.values), 0, decimal=16)
    assert Field_int_loc.unit == "ms"

    Field.unit = "N/m^2"
    Time.unit = "m"
    Field_int = Field.get_data_along("time=integrate", "angle=integrate")
    assert Field_int.unit == "N"
    Time.unit = "s"
    Field.unit = "m"

    # Anti-periodic signal
    Time0 = Time.get_axis_periodic(Nper=1, is_aper=True)
    ta0, at0 = np.meshgrid(Time0.get_values(is_smallestperiod=True), Angle.get_values())
    field0 = A * np.cos(2 * np.pi * f * ta0 + 3 * at0)
    Field0 = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time0, Angle],
        values=field0.T,
    )
    Field_int0 = Field0.get_data_along("time=integrate", "angle")
    assert_array_almost_equal(Field_int0.values, 0, decimal=16)
    Field_mean0 = Field0.get_data_along("time=mean", "angle")
    assert_array_almost_equal(Field_mean0.values, 0, decimal=15)
    Field_sum0 = Field0.get_data_along("time=sum", "angle")
    assert_array_almost_equal(Field_sum0.values, 0, decimal=14)
    Field_rms0 = Field0.get_data_along("time=rms", "angle")
    assert_array_almost_equal(Field_rms0.values, A / np.sqrt(2), decimal=15)

    Field_int_loc0 = Field0.get_data_along("time=integrate_local", "angle")
    assert_array_almost_equal(np.sum(Field_int_loc0.values), 0, decimal=16)

    # Test integrate / sum / mean / rms with and without periodicity
    f = 32.1258
    A = 12.478
    Time1 = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=0.5 / f,
        number=10,
        include_endpoint=False,
        symmetries={"period": 2},
    )
    ta1, at1 = np.meshgrid(Time1.get_values(is_smallestperiod=True), Angle.get_values())
    field1 = A * np.cos(2 * np.pi * f * ta1 + 3 * at1) ** 2
    Field1 = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time1, Angle],
        values=field1.T,
    )

    Time2 = Time1.get_axis_periodic(Nper=1, is_aper=False)
    ta2, at2 = np.meshgrid(Time2.get_values(), Angle.get_values())
    field2 = A * np.cos(2 * np.pi * f * ta2 + 3 * at2) ** 2
    Field2 = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time2, Angle],
        values=field2.T,
    )

    assert_array_almost_equal(Time1.get_values(), Time2.get_values(), decimal=16)
    Field_int1 = Field1.get_data_along("time=integrate", "angle")
    Field_int2 = Field2.get_data_along("time=integrate", "angle")
    assert_array_almost_equal(Field_int1.values, 0.5 * A / f, decimal=15)
    assert_array_almost_equal(Field_int2.values, 0.5 * A / f, decimal=15)
    Field_mean1 = Field1.get_data_along("time=mean", "angle")
    Field_mean2 = Field2.get_data_along("time=mean", "angle")
    assert_array_almost_equal(Field_mean1.values, 0.5 * A, decimal=14)
    assert_array_almost_equal(Field_mean2.values, 0.5 * A, decimal=14)
    Field_rms1 = Field1.get_data_along("time=rms", "angle")
    Field_rms2 = Field2.get_data_along("time=rms", "angle")
    assert_array_almost_equal(Field_rms1.values, np.sqrt(3 * A ** 2 / 8), decimal=14)
    assert_array_almost_equal(Field_rms2.values, np.sqrt(3 * A ** 2 / 8), decimal=14)

    # Test unit change
    Field.unit = "ms"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "ms2"
    Field.unit = "m/s"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "m"
    Field.unit = "m/s2"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "m/s"
    Field.unit = "m/s3"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "m/s2"
    Field.unit = "ms"
    Field_int = Field.get_data_along("time=integrate")
    assert Field_int.unit == "ms2"


@pytest.mark.validation
def test_get_data_along_antiderivate():
    f = 50
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=100,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=200,
        include_endpoint=False,
    )
    ta, at = np.meshgrid(Time.get_values(), Angle.get_values())
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    Field = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )

    # Time derivation
    Field_anti_t = Field.get_data_along("time=antiderivate", "angle")
    assert Field_anti_t.unit == "ms", "wrong unit: " + Field_anti_t.unit
    field_anti_t_check = Field_anti_t.values
    field_anti_t_ref = 5 / (2 * np.pi * f) * np.sin(2 * np.pi * f * ta.T + 3 * at.T)
    assert_array_almost_equal(field_anti_t_check, field_anti_t_ref, decimal=5)

    # Angle derivation
    Field_anti_a = Field.get_data_along("time", "angle=antiderivate")
    assert Field_anti_a.unit == "m2", "wrong unit: " + Field_anti_a.unit
    field_anti_a_check = Field_anti_a.values
    field_anti_a_ref = 5 / 3 * np.sin(2 * np.pi * f * ta.T + 3 * at.T)
    assert_array_almost_equal(field_anti_a_check, field_anti_a_ref, decimal=3)

    Field_int = Field.get_data_along("time=antiderivate", "angle")
    assert Field_int.unit == "ms"
    Field.unit = "ms"
    Field_int = Field.get_data_along("time=antiderivate")
    assert Field_int.unit == "ms2"
    Field.unit = "m/s"
    Field_int = Field.get_data_along("time=antiderivate")
    assert Field_int.unit == "m"
    Field.unit = "m/s2"
    Field_int = Field.get_data_along("time=antiderivate")
    assert Field_int.unit == "m/s"
    Field.unit = "m/s3"
    Field_int = Field.get_data_along("time=antiderivate")
    assert Field_int.unit == "m/s2"
    Field.unit = "ms"
    Field_int = Field.get_data_along("time=antiderivate")
    assert Field_int.unit == "ms2"


@pytest.mark.validation
def test_get_data_along_derivate():
    f = 50
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=100,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=200,
        include_endpoint=False,
    )
    ta, at = np.meshgrid(Time.get_values(), Angle.get_values())
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    Field = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )

    # Time derivation
    Field_diff_t = Field.get_data_along("time=derivate", "angle")
    assert Field_diff_t.unit == "m/s"
    field_diff_t_check = Field_diff_t.values
    field_diff_t_ref = -5 * 2 * np.pi * f * np.sin(2 * np.pi * f * ta.T + 3 * at.T)
    assert_array_almost_equal(field_diff_t_check, field_diff_t_ref, decimal=0)
    # TODO: check and understand discrepancy in field_diff_t_ref/field_diff_t_check

    # Angle derivation
    Field_diff_a = Field.get_data_along("time", "angle=derivate")
    assert Field_diff_a.unit == ""
    field_diff_a_check = Field_diff_a.values
    field_diff_a_ref = -5 * 3 * np.sin(2 * np.pi * f * ta.T + 3 * at.T)
    assert_array_almost_equal(field_diff_a_check, field_diff_a_ref, decimal=1)
    # TODO: check and understand discrepancy in field_diff_a_ref/field_diff_a_check

    # Freqs derivation
    Field_ft = Field.time_to_freq()

    Field_der = Field_ft.get_data_along("freqs=derivate", "angle[0]")
    assert Field_der.unit == "m/s"
    result_ft = Field_ft.get_along("freqs", "angle[0]")
    freqs = result_ft["freqs"]
    field_ft = result_ft["X"]
    assert_array_almost_equal(
        np.squeeze(Field_der.values), field_ft * 2 * 1j * np.pi * freqs
    )
    Field_ft.unit = "m/s"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "m/s2"
    Field_ft.unit = "ms"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "m"
    Field_ft.unit = "ms2"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "ms"
    Field_ft.unit = "ms3"
    Field_der = Field_ft.get_data_along("freqs=derivate", "wavenumber")
    assert Field_der.unit == "ms2"


@pytest.mark.validation
def test_get_data_along_to_linspace():
    """Test to_linspace method that is called in get_data_along"""
    Time = Data1D(name="time", unit="s", values=np.linspace(0, 1, 100))
    Angle = Data1D(name="angle", unit="rad", values=np.array([0]))
    Phase = Data1D(
        name="phase",
        unit="",
        values=["A", "B", "C"],
        is_components=True,
    )

    Time_lin = Time.to_linspace()
    Angle_lin = Angle.to_linspace()
    Phase_lin = Phase.to_linspace()

    # Check transfer of normalizations
    assert isinstance(Time_lin, DataLinspace), "Time axis not a linspace"
    assert isinstance(Angle_lin, Data1D), "Angle axis not a Data1D"
    assert isinstance(Phase_lin, Data1D), "Phase axis not a Data1D"

    assert_array_almost_equal(Time.get_values(), Time_lin.get_values())


@pytest.mark.validation
@pytest.mark.skip(reason="still under development")
def test_get_data_along_integrate_local():

    # Test integrate / sum / mean / rms with and without anti-periodicity
    f = 50
    A = 5
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
    field = A * np.ones(ta.shape)
    Field = DataTime(
        name="Example field",
        symbol="X",
        unit="m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, Angle],
        values=field.T,
    )

    # Time derivation
    Field_anti_t = Field.get_data_along("time=antiderivate", "angle")
    field_anti_t_check = Field_anti_t.values
    field_anti_t_ref = ta.T * A
    assert_array_almost_equal(field_anti_t_check, field_anti_t_ref, decimal=5)

    Field_int_loc = Field.get_along("time=integrate_local", "angle")["X"]
    assert_equal(Field_int_loc.shape, (10, 20))

    DtA = A / (10 * f)
    Field_int_loc = Field.get_along("time=integrate_local", "angle[0]")["X"]
    assert_array_almost_equal(np.sum(Field_int_loc.values), 0, decimal=16)
    assert Field_int_loc.unit == "ms"


@pytest.mark.validation
def test_get_data_along_integrate_local_pattern():

    # Test integration per step with DataPattern
    f = 50
    A = 5
    Nt = 3
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=Nt,
        include_endpoint=False,
    )

    z = DataPattern(
        name="z",
        unit="m",
        values=np.array([-0.045, -0.09]),
        rebuild_indices=[1, 1, 0, 0, 0, 0, 1, 1],
        unique_indices=[2, 0],
        values_whole=np.array([-0.09, -0.045, -0.045, 0.0, 0.0, 0.045, 0.045, 0.09]),
        is_step=True,
    )

    time = Time.get_values()
    field = np.zeros((Nt, 2))
    field[:, 0] = A * np.cos(2 * np.pi * f * time)
    field[:, 1] = 0.5 * A * np.cos(2 * np.pi * f * time)

    Field = DataTime(
        name="Example field",
        symbol="X",
        unit="T/m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, z],
        values=field,
    )

    # Field.plot_3D_Data("time", "z")
    # Field.plot_2D_Data("z", "time[0]")
    Field_int_loc = Field.get_data_along("time", "z=integrate_local")
    assert_equal(Field_int_loc.values.shape, (Nt, 4))
    assert_array_almost_equal(
        2 * Field_int_loc.values[:, [0, 3]], Field_int_loc.values[:, [1, 2]]
    )

    z2 = DataPattern(
        name="z",
        unit="m",
        values=np.array([-0.09, -0.045, 0.0, 0.045, 0.09]),
        rebuild_indices=[0, 1, 2, 3, 4],
        unique_indices=[0, 1, 2, 3, 4],
        values_whole=np.array([-0.09, -0.045, 0.0, 0.045, 0.09]),
        is_step=False,
    )

    field2 = np.zeros((Nt, 5))
    field2[:, 0] = A * np.cos(2 * np.pi * f * time)
    field2[:, 1] = 0.8 * A * np.cos(2 * np.pi * f * time)
    field2[:, 2] = 0.6 * A * np.cos(2 * np.pi * f * time)
    field2[:, 3] = 0.4 * A * np.cos(2 * np.pi * f * time)
    field2[:, 4] = 0.2 * A * np.cos(2 * np.pi * f * time)

    Field2 = DataTime(
        name="Example field 2",
        symbol="X",
        unit="T/m",
        normalizations={"ref": Norm_ref(ref=2e-5)},
        axes=[Time, z2],
        values=field2,
    )

    Field2.plot_3D_Data("time", "z")
    Field2.plot_2D_Data("z", "time[0]")
    Field_int_loc2 = Field2.get_data_along("time", "z=integrate_local")
    assert_equal(Field_int_loc2.values.shape, (Nt, 4))
    # assert_array_almost_equal(
    #     0.8 * Field_int_loc2.values[:, 0], Field_int_loc2.values[:, 1]
    # )


if __name__ == "__main__":
    # test_get_data_along_single()
    # test_get_data_along_integrate()
    # test_get_data_along_derivate()
    # test_get_data_along_antiderivate()
    # test_get_data_along_to_linspace()
    # test_get_data_along_integrate_local()
    test_get_data_along_integrate_local_pattern()