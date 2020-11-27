import pytest
from SciDataTool import DataTime, DataFreq, DataLinspace, Data1D
import numpy as np
from numpy.testing import assert_array_almost_equal


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
    field = 3 * np.cos(2 * np.pi * f * time + 3 * np.pi / 4)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
        unit="m",
    )
    result = Field.get_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0, 50, 100]), result["freqs"])
    assert_array_almost_equal(
        np.array([0, 3 * np.cos(3 * np.pi / 4) * (1 - 1j), 0]), result["X"]
    )

    result = Field.get_magnitude_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0, 3, 0]), result["X"])

    result = Field.get_phase_along("freqs=[0,100]")
    assert_array_almost_equal(np.pi, result["X"][0])

    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(Field_FT.get_along("time")["X"], field)


@pytest.mark.validation
def test_fft2d():
    f = 50
    time = np.linspace(0, 1 / f, 5, endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1 / f,
        number=5,
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
    field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m",
    )
    result = Field.get_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([0, 5, 0]), result["X"])

    result = Field.get_along("wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0, 1, 2, 3, 4]), result["wavenumber"])
    assert_array_almost_equal(np.array([0, 0, 0, 5, 0]), result["X"])

    result = Field.get_along("freqs=[0,100]", "wavenumber=[-3,3]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([-3, -2, -1, 0, 1, 2, 3]), result["wavenumber"])
    X = np.zeros((3, 7))
    X[1, 6] = 5  # The negative freq -f is folded on +f to keep signal energy constant
    assert_array_almost_equal(X, result["X"])

    result = Field.get_along("freqs=[0,100]", "wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([0, 1, 2, 3, 4]), result["wavenumber"])
    X = np.zeros((3, 5))
    X[
        1, 3
    ] = 10  # The negative wavenumber -3 is folded on +3 to keep signal energy constant
    assert_array_almost_equal(X, result["X"])

    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(Field_FT.get_along("angle", "time")["X"], field)


@pytest.mark.validation
def test_ifft1d():
    f = 50
    freqs = np.array([-100, -50, 0, 50, 100])
    Freqs = Data1D(name="freqs", unit="Hz", values=freqs)

    #%% Test1 : Random complex signal
    field = np.random.random(5) + 1j * np.random.random(5)
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs],
        values=field,
        unit="m",
    )
    result = Field.get_along("time")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 1 / f, 5, endpoint=False), time)

    Nf = len(freqs)
    field_ift = np.zeros((5))
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
            3 + 5 * 1j,
            0,
            3 - 5 * 1j,
            0,
        ]
    )
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs],
        values=field,
        unit="m",
    )
    result = Field.get_along("time")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 1 / f, 5, endpoint=False), time)

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
    freqs = np.array([-100, -50, 0, 50, 100])
    Freqs = Data1D(name="freqs", unit="Hz", values=freqs)
    wavenumber = np.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    Wavenumber = Data1D(name="wavenumber", unit="dimless", values=wavenumber)
    X = np.zeros((5, 9))
    X[1, 1] = 5
    X[3, 7] = 5
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs, Wavenumber],
        values=X,
        unit="m",
    )
    result = Field.get_along("time", "angle")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0, 1 / f, 5, endpoint=False), time)
    angle = result["angle"]
    assert_array_almost_equal(np.linspace(0, 2 * np.pi, 9, endpoint=False), angle)
    Xangle, Xtime = np.meshgrid(angle, time)
    field_ift = (
        2 * 5 * np.cos(2 * np.pi * f * Xtime + 3 * Xangle)
    )  # 2 times the real part
    assert_array_almost_equal(field_ift, result["X"])

    Field_IFT = Field.freq_to_time()
    assert_array_almost_equal(Field_IFT.get_along("wavenumber", "freqs")["X"], X)

    Field_2 = Field_IFT.time_to_freq()
    assert_array_almost_equal(Field_2.get_along("angle", "time")["X"], field_ift)

    #%% Test 2
    X = np.random.random((5, 9)) + np.random.random((5, 9)) * 1j

    # The signal is a complex conjugate along freqs axis, as mag field should be
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs, Wavenumber],
        values=X,
        unit="m",
    )
    result = Field.get_along("time", "angle")

    Nr = len(wavenumber)
    Nf = len(freqs)
    field_ift = np.zeros((5, 9))
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
    wavenumber_test = result_fft["wavenumber"]

    Nr = len(wavenumber)
    Nf = len(freqs)
    field_ift = np.zeros((5, 9))

    for ir in range(Nr):
        r = wavenumber[ir]

        for ifrq in range(len(freqs_test)):
            fit = freqs_test[ifrq]
            field_ift = field_ift + abs(X_test[ifrq, ir]) * np.cos(
                (2 * np.pi * fit * Xtime + r * Xangle + np.angle(X_test[ifrq, ir]))
            )

    assert_array_almost_equal(field_ift, result["X"])


@pytest.mark.validation
def test_fft2d_period():
    f = 50
    time = np.linspace(0, 1 / f, 10, endpoint=False)
    Time = Data1D(name="time", unit="s", values=time, symmetries={"period": 5})
    angle = np.linspace(0, 2 * np.pi, 20, endpoint=False)

    at, ta = np.meshgrid(angle, time)
    Angle = Data1D(name="angle", unit="rad", values=angle, symmetries={"period": 4})
    field = 5 * np.cos(2 * np.pi * f * ta + at)
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
    assert_array_almost_equal(np.array([0, 5, 0]), result["X"])

    result = Field.get_along("wavenumber=[0,10]")
    assert_array_almost_equal(np.array([0, 4, 8]), result["wavenumber"])
    assert_array_almost_equal(np.array([0, 5, 0]), result["X"])

    result = Field.get_along("freqs=[0,100]", "wavenumber=[-10,10]")
    assert_array_almost_equal(np.array([0, f, 2 * f]), result["freqs"])
    assert_array_almost_equal(np.array([-8, -4, 0, 4, 8]), result["wavenumber"])
    X = np.zeros((3, 5))
    X[1, 3] = 5
    assert_array_almost_equal(X, result["X"])

    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(Field_FT.get_along("angle", "time")["X"], field)
