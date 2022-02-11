from pandas import NA
import pytest
from SciDataTool import (
    DataTime,
    DataFreq,
    DataLinspace,
    Data1D,
    VectorField,
    Norm_indices,
)
import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy import zeros, exp, real, pi, take, insert, delete
from numpy.fft import rfftn, irfftn, fftshift, fftn, ifftshift, ifftn


@pytest.mark.validation
def test_fft2_remove_periodicity():
    f = 50
    Nt_tot = 16
    Na_tot = 20
    time = np.linspace(0, 1 / (2 * f), Nt_tot, endpoint=False)
    Time = Data1D(name="time", unit="s", values=time, symmetries={"antiperiod": 4})
    angle = np.linspace(0, 2 * np.pi, Na_tot, endpoint=False)
    Angle = Data1D(name="angle", unit="rad", values=angle, symmetries={"period": 4})

    field = np.random.random((Nt_tot, Na_tot))

    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )

    angle_new = Angle.get_values(is_oneperiod=True, is_antiperiod=False)

    time_new = Time.get_values(
        is_oneperiod=False,
        is_antiperiod=False,
    )

    # Load magnetic flux
    field_new = Field.get_along(
        "time=axis_data",
        "angle=axis_data",
        axis_data={"time": time_new, "angle": angle_new},
    )["X"]

    Time2 = Data1D(name="time", unit="s", values=time_new, symmetries={"period": 2})
    Angle2 = Data1D(name="angle", unit="rad", values=angle_new)

    Field_new = DataTime(
        name="field",
        symbol="X",
        axes=[Time2, Angle2],
        values=field_new,
        unit="m",
    )

    result_fft = Field_new.get_along("freqs", "wavenumber")
    X_test = result_fft["X"]
    freqs = result_fft["freqs"]
    wavenumber = result_fft["wavenumber"]

    Nr = len(wavenumber)
    Nf = len(freqs)

    # Check the FFT2 reconstruction of the new object
    field_ift = np.zeros((len(time_new), len(angle_new)))
    Xangle, Xtime = np.meshgrid(angle_new, time_new)

    for ir in range(Nr):
        r = wavenumber[ir]
        for ifrq in range(Nf):
            fit = freqs[ifrq]
            field_ift = field_ift + abs(X_test[ifrq, ir]) * np.cos(
                (2 * np.pi * fit * Xtime + r * Xangle + np.angle(X_test[ifrq, ir]))
            )

    assert_array_almost_equal(field_ift, field_new)

    # Compare with the initial field
    field_ift = np.zeros((len(time), len(angle)))
    Xangle, Xtime = np.meshgrid(angle, time)

    for ir in range(Nr):
        r = wavenumber[ir]
        for ifrq in range(Nf):
            fit = freqs[ifrq]
            field_ift = field_ift + abs(X_test[ifrq, ir]) * np.cos(
                (2 * np.pi * fit * Xtime + r * Xangle + np.angle(X_test[ifrq, ir]))
            )

    assert_array_almost_equal(field_ift, field)


@pytest.mark.validation
def test_compare_rfft_fft_irfft_ifft():

    Nt = 20

    X = np.random.random((Nt))
    size = Nt

    # RFFT
    values_FT = rfftn(X)
    slice_0 = take(values_FT, 0)
    slice_0 *= 0.5
    other_values = delete(values_FT, 0)
    values_FT = insert(other_values, 0, slice_0)
    values_FT = 2.0 * fftshift(values_FT, axes=[]) / size

    # FFT
    values_FT2 = fftn(X)
    values_FT2 = fftshift(values_FT2) / size

    assert_array_almost_equal(values_FT[1:-1], values_FT2[11:] * 2)

    # IRFFT
    values = values_FT * (size / 2)
    values = ifftshift(values, axes=[])
    slice_0 = take(values, 0)
    slice_0 *= 2
    other_values = delete(values, 0)
    values = insert(other_values, 0, slice_0)
    # values = ifftshift(values/2, axes=axes[:-1]) * size
    values_IFT = irfftn(values)

    # IFFT
    values2 = ifftshift(values_FT2) * size
    values_IFT2 = ifftn(values2)

    assert_array_almost_equal(values_IFT, values_IFT2)


@pytest.mark.validation
def test_fft1d():
    f = 50
    time = np.linspace(0, 1 / f, 10, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=10,
        include_endpoint=False,
    )
    field = 2 + 3 * np.cos(2 * np.pi * f * time + 3 * np.pi / 4)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
        unit="m",
    )

    Field_FT = Field.time_to_freq()
    result = Field_FT.get_along("time")
    assert_array_almost_equal(result["X"], field)
    assert_array_almost_equal(result["time"], time)

    result = Field.get_along("freqs<100")
    assert_array_almost_equal(np.array([0, 50, 100]), result["freqs"])
    assert_array_almost_equal(
        np.array([2, 3 * np.cos(3 * np.pi / 4) * (1 - 1j), 0]), result["X"]
    )

    result = Field.get_magnitude_along("freqs<100")
    assert_array_almost_equal(np.array([2, 3, 0]), result["X"])

    result = Field.get_phase_along("freqs<100")
    assert_array_almost_equal(0, result["X"][0])
    assert_array_almost_equal(3 * np.pi / 4, result["X"][1])

    Field2 = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
        unit="m",
        is_real=False,
    )

    result = Field2.get_along("freqs")

    Field_FT = Field2.time_to_freq()
    result = Field_FT.get_along("time")
    assert_array_almost_equal(result["X"], field)
    assert_array_almost_equal(result["time"], time)

    Field3 = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
        unit="m",
        is_real=True,
    )

    Field_FT = Field3.time_to_freq()
    result = Field_FT.get_along("time")
    assert_array_almost_equal(result["X"], field)
    assert_array_almost_equal(result["time"], time)


@pytest.mark.validation
def test_fft2d():

    #%% Test&
    f = 50
    time = np.linspace(0, 1 / f, 6, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=6,
        include_endpoint=False,
    )
    angle = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    at, ta = np.meshgrid(angle, time)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=10,
        include_endpoint=False,
    )
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at) - 2 * np.cos(-at)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
        is_real=True,  # Default value, store only positive frequencies to save memory space
    )

    result = Field.get_along("freqs")
    assert_array_almost_equal(np.array([0, f, 2 * f, 3 * f]), result["freqs"])

    result = Field.get_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([-2, 5, 0]), result["X"])

    Field.is_real = False  # Desactivate the storage of "real" time signal, such all the spectrum is stored
    result = Field.get_along("freqs")
    assert_array_almost_equal(
        np.array([-3 * f, -2 * f, -f, 0, f, 2 * f]), result["freqs"]
    )

    result = Field.get_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(
        np.array([-2, 5 / 2, 0]), result["X"]
    )  # Half of the signal is still at -f

    Field.is_real = True
    result = Field.get_along("wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0, 1, 2, 3, 4]), result["wavenumber"])
    assert_array_almost_equal(
        np.array([0, -2, 0, 5, 0]), result["X"]
    )  # Spatial FFT of the cosine, 2 harmonics

    result = Field.get_along("freqs=[0,100]", "wavenumber")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(
        np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]), result["wavenumber"]
    )
    X = np.zeros((3, 10))
    X[1, 8] = 5  # The negative freq -f is folded on +f to keep signal energy constant
    X[0, 4] = -1
    X[0, 6] = -1
    assert_array_almost_equal(X, result["X"])

    result = Field.get_along("freqs=[0,100]", "wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([0, 1, 2, 3, 4]), result["wavenumber"])
    X = np.zeros((3, 5))
    X[
        1, 3
    ] = 5  # The negative wavenumber -3 is folded on +3 to keep signal energy constant

    X[0, 1] = -1
    assert_array_almost_equal(X, result["X"])

    result = Field.get_along("wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0, 1, 2, 3, 4]), result["wavenumber"])
    assert_array_almost_equal(
        np.array([0, -2, 0, 5, 0]), result["X"]
    )  # It is a 1d fft on angle, so there are two equal wavenumbers at +3 and -3

    # Warning: following only work for even sized time vector
    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(Field_FT.get_along("angle", "time")["X"], field)


@pytest.mark.validation
def test_ifft1d():
    f = 50
    freqs = np.array([-150, -100, -50, 0, 50, 100])
    Freqs = Data1D(name="freqs", unit="Hz", values=freqs)

    #%% Test1 : Random complex signal
    field = np.random.random(6) + 1j * np.random.random(6)
    Field = DataFreq(
        name="field", symbol="X", axes=[Freqs], values=field, unit="m", is_real=False
    )
    result = Field.get_along("time")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 1 / f, 6, endpoint=False), time)

    Nf = len(freqs)
    field_ift = np.zeros((6))
    for ifrq in range(Nf):
        fit = freqs[ifrq]
        field_ift = field_ift + (field[ifrq] * np.exp(1j * (2 * np.pi * fit * time)))

    assert_array_almost_equal(field_ift, result["X"])

    Field_IFT = Field.freq_to_time()
    assert_array_almost_equal(Field_IFT.get_along("freqs")["X"], field)

    #%% Test2 : Real-time signal
    field = np.array(
        [
            0,
            0,
            3 + 5 * 1j,
            0,
            3 - 5 * 1j,
            0,
        ]
    )
    Field = DataFreq(
        name="field", symbol="X", axes=[Freqs], values=field, unit="m", is_real=False
    )
    result = Field.get_along("time")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 1 / f, 6, endpoint=False), time)

    field_ift = abs(3 + 5 * 1j) * np.cos(
        -2 * np.pi * f * time + np.angle(3 + 5 * 1j)
    ) + abs(3 - 5 * 1j) * np.cos(2 * np.pi * f * time + np.angle(3 - 5 * 1j))

    assert_array_almost_equal(field_ift, result["X"])

    Field_IFT = Field.freq_to_time()
    assert_array_almost_equal(Field_IFT.get_along("freqs")["X"], field)


@pytest.mark.validation
def test_ifft2d():

    #%% Test 1
    f = 50
    freqs = np.array([0, 50, 100, 150])
    Freqs = Data1D(name="freqs", unit="Hz", values=freqs)
    wavenumber = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4])
    Wavenumber = Data1D(name="wavenumber", unit="dimless", values=wavenumber)
    X = np.zeros((4, 10))
    X[1, 2] = 5  # Only the positive frequency harmonic of the real signal
    # X[4, 7] = 5
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs, Wavenumber],
        values=X,
        unit="m",
        is_real=True,
    )
    result = Field.get_along("time", "angle")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 1 / f, 6, endpoint=False), time)
    angle = result["angle"]
    assert_array_almost_equal(np.linspace(0, 2 * np.pi, 10, endpoint=False), angle)
    Xangle, Xtime = np.meshgrid(angle, time)
    field_ift = 5 * np.cos(2 * np.pi * f * Xtime - 3 * Xangle)  # 2 times the real part
    assert_array_almost_equal(field_ift, result["X"])

    Field_IFT = Field.freq_to_time()
    assert_array_almost_equal(Field_IFT.get_along("wavenumber", "freqs")["X"], X)

    Field_2 = Field_IFT.time_to_freq()
    assert_array_almost_equal(Field_2.get_along("angle", "time")["X"], field_ift)

    #%% Test 2
    X = np.random.random((6, 10)) + np.random.random((6, 10)) * 1j
    freqs = np.array([-150, -100, -50, 0, 50, 100])
    Freqs = Data1D(name="freqs", unit="Hz", values=freqs)
    wavenumber = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4])
    Wavenumber = Data1D(name="wavenumber", unit="dimless", values=wavenumber)
    # The signal is a complex conjugate along freqs axis, as mag field should be
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs, Wavenumber],
        values=X,
        unit="m",
        is_real=False,
    )
    result = Field.get_along("time", "angle")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 1 / f, 6, endpoint=False), time)
    angle = result["angle"]
    assert_array_almost_equal(np.linspace(0, 2 * np.pi, 10, endpoint=False), angle)
    Xangle, Xtime = np.meshgrid(angle, time)

    Nr = len(wavenumber)
    Nf = len(freqs)
    field_ift = np.zeros((6, 10))
    for ir in range(Nr):
        r = wavenumber[ir]
        for ifrq in range(Nf):
            fit = freqs[ifrq]
            field_ift = field_ift + (
                X[ifrq, ir] * np.exp(1j * (2 * np.pi * fit * Xtime + r * Xangle))
            )

    assert_array_almost_equal(field_ift, result["X"])

    #%% Test 3 : Real signal
    r = 2
    my_field = np.cos(r * Xangle + 2 * np.pi * f * Xtime + np.pi / 6) + np.cos(
        -2 * r * Xangle + 2 * np.pi * 2 * f * Xtime
    )

    Time = Data1D(name="time", unit="s", values=time)
    Angle = Data1D(name="angle", unit="rad", values=angle)
    # The signal is a complex conjugate along freqs axis, as mag field should be

    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=my_field,
        unit="m",
    )

    result = Field.get_along("time", "angle")
    result_fft = Field.get_along("freqs>0", "wavenumber")
    X_test = result_fft["X"]
    freqs_test = result_fft["freqs"]

    Nr = len(wavenumber)
    Nf = len(freqs)
    field_ift = np.zeros((6, 10))

    for ir in range(Nr):
        r = wavenumber[ir]

        for ifrq in range(len(freqs_test)):
            fit = freqs_test[ifrq]
            field_ift = field_ift + abs(X_test[ifrq, ir]) * np.cos(
                (2 * np.pi * fit * Xtime + r * Xangle + np.angle(X_test[ifrq, ir]))
            )

    assert_array_almost_equal(field_ift, result["X"])


@pytest.mark.validation
def test_ifft2d_vector():

    f = 50
    time = np.linspace(0, 1 / f, 6, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=6,
        include_endpoint=False,
    )
    angle = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    at, ta = np.meshgrid(angle, time)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=10,
        include_endpoint=False,
    )

    field = (
        2
        + 5 * np.cos(2 * np.pi * f * ta + 3 * at)
        + 2 * np.cos(-2 * np.pi * f * ta + at)
    )

    Rad = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )

    arg_list = ["freqs", "angle"]
    result_freq = Rad.get_along(*arg_list)
    X_w = result_freq["X"]
    freqs = result_freq["freqs"]
    Nf = len(freqs)
    XP = zeros(field.shape)
    Xangle, Xtime = np.meshgrid(angle, time)

    # Since only positive frequency were extracted, the correct sum must be on the the real part
    for ifrq in range(Nf):
        frq = freqs[ifrq]
        XP = XP + real(X_w[ifrq, :] * exp(1j * 2 * pi * frq * Xtime))

    assert_array_almost_equal(XP, field, decimal=5)

    Tan = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=0 * field,
        unit="m",
    )

    Vector = VectorField(
        name="Air gap Surface Force",
        symbol="AGSF",
    )
    # Radial component
    Vector.components["radial"] = Rad
    # Tangential component
    Vector.components["tangential"] = Tan

    arg_list = ["time", "angle"]
    result = Vector.get_rphiz_along(*arg_list)
    X = result["radial"]
    time = result["time"]

    arg_list = ["freqs", "angle"]
    result_freq = Vector.get_rphiz_along(*arg_list)
    X_w = result_freq["radial"]
    freqs = result_freq["freqs"]
    Nf = len(freqs)

    XP = zeros(X.shape)
    Xangle, Xtime = np.meshgrid(angle, time)

    # Since only positive frequency were extracted, the correct sum must be on the the real part
    for ifrq in range(Nf):
        frq = freqs[ifrq]
        XP = XP + real(X_w[ifrq, :] * exp(1j * 2 * pi * frq * Xtime))

    assert_array_almost_equal(XP, X, decimal=5)

    result_fft = Vector.get_rphiz_along("freqs", "wavenumber")
    X_test = result_fft["radial"]
    freqs_test = result_fft["freqs"]
    wavenumber = result_fft["wavenumber"]

    Nr = len(wavenumber)
    Nf = len(freqs)
    field_ift = np.zeros((6, 10))

    for ir in range(Nr):
        r = wavenumber[ir]
        for ifrq in range(len(freqs_test)):
            fit = freqs_test[ifrq]
            field_ift = field_ift + abs(X_test[ifrq, ir]) * np.cos(
                (2 * np.pi * fit * Xtime + r * Xangle + np.angle(X_test[ifrq, ir]))
            )

    assert_array_almost_equal(field_ift, X)

    field_ift = np.zeros((6, 10))
    for ir in range(Nr):
        r = wavenumber[ir]
        for ifrq in range(len(freqs_test)):
            fit = freqs_test[ifrq]
            field_ift = field_ift + real(
                X_test[ifrq, ir] * np.exp(1j * (2 * np.pi * fit * Xtime + r * Xangle))
            )

    assert_array_almost_equal(field_ift, X)


@pytest.mark.validation
def test_ifft2d_random():

    f = 50
    nt = 7 * 2
    na = 7 * 2
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=nt,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=na,
        include_endpoint=False,
    )

    field = np.random.random((nt, na))
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )

    Field_FT = Field.time_to_freq()
    arg_list = ["time", "angle"]
    assert_array_almost_equal(Field_FT.get_along(*arg_list)["X"], field)


@pytest.mark.validation
def test_ifft1d_random():
    # %%
    f = 50
    Nt = 20
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=Nt,
        include_endpoint=False,
    )

    X = np.random.random((Nt))
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=X,
        unit="m",
    )

    Field_ft = Field.time_to_freq()
    result = Field_ft.get_along("time")
    assert_array_almost_equal(X, result["X"])


@pytest.mark.validation
def test_fft2d_period():
    # %%
    f = 50
    time = np.linspace(0, 1 / f, 10, endpoint=False)
    Time = Data1D(name="time", unit="s", values=time, symmetries={"period": 5})
    angle = np.linspace(0, 2 * np.pi, 20, endpoint=False)

    at, ta = np.meshgrid(angle, time)
    Angle = Data1D(name="angle", unit="rad", values=angle, symmetries={"period": 4})
    field = 2 + 5 * np.cos(2 * np.pi * f * ta + at)
    # field = 5*np.cos(2*np.pi*f*time)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )
    result = Field.get_magnitude_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([2, 5, 0]), result["X"])

    result = Field.get_along("wavenumber=[0,10]")
    assert_array_almost_equal(np.array([0, 4, 8]), result["wavenumber"])
    assert_array_almost_equal(
        np.array([2, 5, 0]), result["X"]
    )  # FFT spatial at 1 time -> Half of the signal

    result = Field.get_along("freqs=[0,100]", "wavenumber=[-10,10]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([-8, -4, 0, 4, 8]), result["wavenumber"])
    X = np.zeros((3, 5))
    X[1, 3] = 5
    X[0, 2] = 2
    assert_array_almost_equal(X, result["X"])

    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(
        Field_FT.get_along("angle", "time")["X"], Field.get_along("angle", "time")["X"]
    )


@pytest.mark.validation
def test_ifft2d_period():
    f = 50
    freqs = np.array([0, 50, 100, 150])
    Freqs = Data1D(name="freqs", unit="Hz", values=freqs, symmetries={"period": 10})
    wavenumber = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4])
    Wavenumber = Data1D(name="wavenumber", unit="dimless", values=wavenumber)
    X = np.zeros((4, 10))
    X[1, 2] = 5  # Only the positive frequency harmonic of the real signal
    # X[4, 7] = 5
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs, Wavenumber],
        values=X,
        unit="m",
        is_real=True,
    )
    result = Field.get_along("time", "angle")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 10 / f, 60, endpoint=False), time)
    angle = result["angle"]
    assert_array_almost_equal(np.linspace(0, 2 * np.pi, 10, endpoint=False), angle)
    Xangle, Xtime = np.meshgrid(angle, time)
    field_ift = 5 * np.cos(2 * np.pi * f * Xtime - 3 * Xangle)  # 2 times the real part
    assert_array_almost_equal(field_ift, result["X"])

    result = Field.get_along("time=0.03", "angle")
    time0 = result["time"]
    assert_array_almost_equal(0.03, time0)
    angle = result["angle"]
    assert_array_almost_equal(np.linspace(0, 2 * np.pi, 10, endpoint=False), angle)
    assert_array_almost_equal(field_ift[9, :], result["X"])


@pytest.mark.validation
def test_init_new_object():
    # %%
    f = 50
    nt = 7 * 2
    na = 7 * 2
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=nt,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2 * np.pi,
        number=na,
        include_endpoint=False,
    )

    field = np.random.random((nt, na))
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )

    arg_list = ["freqs", "wavenumber"]
    result = Field.get_along(*arg_list)
    X_FT = result["X"]
    freqs = result["freqs"]
    wavenumber = result["wavenumber"]

    Freqs = Data1D(name="freqs", unit="Hz", values=freqs)
    Wavenumber = Data1D(name="wavenumber", unit="", values=wavenumber)
    new_Field = DataTime(
        name="field2", unit="m", symbol="XX", axes=[Freqs, Wavenumber], values=X_FT
    )

    assert_array_almost_equal(
        new_Field.get_along("angle", "time")["XX"],
        Field.get_along("angle", "time")["X"],
    )


@pytest.mark.validation
def test_fft2_anti_period():
    # %%
    f = 50
    time = np.linspace(0, 1 / (2 * f), 10, endpoint=False)
    Time = Data1D(name="time", unit="s", values=time, symmetries={"antiperiod": 4})
    angle = np.linspace(0, 2 * np.pi, 20, endpoint=False)

    at, ta = np.meshgrid(angle, time)
    Angle = Data1D(name="angle", unit="rad", values=angle, symmetries={"period": 4})
    field = 5 * np.cos(2 * np.pi * f * ta + at)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )

    result = Field.get_magnitude_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([0, 5, 0]), result["X"])

    result = Field.get_along("wavenumber=[0,10]")
    assert_array_almost_equal(np.array([0, 4, 8]), result["wavenumber"])
    assert_array_almost_equal(
        np.array([0, 5, 0]), result["X"]
    )  # FFT spatial at 1 time -> Half of the signal

    result = Field.get_along("freqs=[0,100]", "wavenumber=[-10,10]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([-8, -4, 0, 4, 8]), result["wavenumber"])
    X = np.zeros((3, 5))
    X[1, 3] = 5

    assert_array_almost_equal(X, result["X"])

    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(
        Field_FT.get_along("angle", "time")["X"], Field.get_along("angle", "time")["X"]
    )

    Field_FT = Field_FT.freq_to_time()
    assert_array_almost_equal(
        Field_FT.get_along("angle", "time")["X"], Field.get_along("angle", "time")["X"]
    )


@pytest.mark.validation
def test_fft2_anti_period_random():
    # %%
    f = 50
    time = np.linspace(0, 1 / (2 * f), 10, endpoint=False)
    Time = Data1D(name="time", unit="s", values=time, symmetries={"antiperiod": 4})
    angle = np.linspace(0, 2 * np.pi, 20, endpoint=False)
    Angle = Data1D(name="angle", unit="rad", values=angle, symmetries={"period": 4})

    field = np.random.random((10, 20))

    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )

    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(
        Field_FT.get_along("angle", "time")["X"], Field.get_along("angle", "time")["X"]
    )

    assert_array_almost_equal(
        Field_FT.get_along("angle", "time")["time"],
        Field.get_along("angle", "time")["time"],
    )

    Field_FT = Field_FT.freq_to_time()
    assert_array_almost_equal(
        Field_FT.get_along("angle", "time")["X"], Field.get_along("angle", "time")["X"]
    )


@pytest.mark.validation
def test_fft1d_non_uniform(per_a=2, is_apera=True, is_add_zero_freq=True):
    """check non uniform fft1d
    TODO: solve bug for a single frequency vector"""
    # %%
    f = 50
    Na = 4 * 10
    slip = 0.01
    Nt = 100
    A0 = 10

    sym_dict = dict()
    per_a0 = per_a
    if is_apera:
        per_a *= 2
        sym_dict["antiperiod"] = per_a
    elif per_a > 1:
        sym_dict["period"] = per_a

    # Creating the data object
    Phase = DataLinspace(
        name="phase",
        unit="rad",
        initial=0,
        final=2 * pi / per_a,
        number=int(Na / per_a),
        include_endpoint=False,
        symmetries=sym_dict,
        normalizations={"bar_id": Norm_indices()},
        is_overlay=True,
    )

    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=Nt,
        symmetries={"antiperiod": 4},
    )

    angle_bars = Phase.get_values(is_smallestperiod=True)

    if is_add_zero_freq:
        values = np.zeros((2, angle_bars.size), dtype=complex)
        values[1, :] = A0 * np.exp(1j * per_a0 * angle_bars)
        freqs_val = np.array([0, slip * f])
    else:
        values = A0 * np.exp(1j * per_a0 * angle_bars[None, :])
        freqs_val = np.array([slip * f])

    Freqs = Data1D(
        name="freqs",
        symbol="",
        unit="Hz",
        values=freqs_val,
        normalizations=dict(),
    )

    Data = DataFreq(
        name="field", unit="A", symbol="X", axes=[Freqs, Phase], values=values
    )

    val_time = Data.get_data_along(
        "time=axis_data", "phase", axis_data={"time": Time.get_values()}
    )

    # Plot
    # val_time.plot_2D_Data("phase", "time[0]", type_plot="bargraph")
    # val_time.plot_2D_Data("time", "phase[0,1,2,3]")

    val_check = A0 * np.cos(2 * np.pi * slip * f * Time.get_values())
    assert_array_almost_equal(val_time.values[:, 0], val_check)


if __name__ == "__main__":
    # test_ifft2d_period()
    test_fft1d_non_uniform(is_add_zero_freq=True)
    test_fft1d_non_uniform(is_add_zero_freq=False)
