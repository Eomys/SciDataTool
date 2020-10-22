import pytest
from SciDataTool import DataTime, DataFreq, DataLinspace, Data1D
import numpy as np
from numpy.testing import assert_array_almost_equal


@pytest.mark.validation
def test_fft1d():
    f = 50
    time = np.linspace(0,1/f,10,endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1/f,
        number=10,
        include_endpoint=False,
    )
    field = 3*np.cos(2*np.pi*f*time + 3*np.pi/4)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
        unit="m",
    )
    result = Field.get_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0,50,100]), result["freqs"])
    assert_array_almost_equal(np.array([0,3*np.cos(3*np.pi/4)*(1-1j),0]), result["X"])
    
    result = Field.get_magnitude_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0,3,0]), result["X"])
    
    result = Field.get_phase_along("freqs=[0,100]")
    assert_array_almost_equal(np.pi, result["X"][0])
    
    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(Field_FT.get_along("time")["X"], field)


@pytest.mark.validation
def test_fft2d():
    f = 50
    time = np.linspace(0,1/f,10,endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=1/f,
        number=10,
        include_endpoint=False,
    )
    angle = np.linspace(0,2*np.pi,20,endpoint=False)
    ta, at = np.meshgrid(time, angle)
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2*np.pi,
        number=20,
        include_endpoint=False,
    )
    field = 5*np.cos(2*np.pi*f*ta + 3*at)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Angle, Time],
        values=field,
        unit="m",
    )
    result = Field.get_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0,f,2*f]), result["freqs"])
    assert_array_almost_equal(np.array([0,5,0]), result["X"])
    
    result = Field.get_along("wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0,1,2,3,4]), result["wavenumber"])
    assert_array_almost_equal(np.array([0,0,0,5,0]), result["X"])
    
    result = Field.get_along("freqs=[0,100]", "wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0,f,2*f]), result["freqs"])
    assert_array_almost_equal(np.array([0,1,2,3,4]), result["wavenumber"])
    X = np.zeros((5,3))
    X[3,1] = 5
    assert_array_almost_equal(X, result["X"])
    
    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(Field_FT.get_along("angle", "time")["X"], field)


@pytest.mark.validation
def test_ifft1d():
    f=50
    freqs = np.array([-100,-50,0,50,100])
    Freqs = Data1D(
        name="freqs",
        unit="Hz",
        values = freqs
    )
    field = np.array([0,3+5*1j,0,3-5*1j,0,])
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Freqs],
        values=field,
        unit="m",
    )
    result = Field.get_along("time")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0,1/f,5,endpoint=False), time)
    field_ift = 3*np.cos(2*np.pi*f*time) + 5*np.sin(2*np.pi*f*time)
    assert_array_almost_equal(field_ift, result["X"])
    
    Field_IFT = Field.freq_to_time()
    assert_array_almost_equal(Field_IFT.get_along("freqs")["X"], field)


@pytest.mark.validation
def test_ifft2d():    
    f = 50
    freqs = np.array([-100,-50,0,50,100])
    Freqs = Data1D(
        name="freqs",
        unit="Hz",
        values = freqs
    )
    wavenumber = np.array([-4,-3,-2,-1,0,1,2,3,4])
    Wavenumber = Data1D(
        name="wavenumber",
        unit="dimless",
        values = wavenumber
    )
    X = np.zeros((9,5))
    X[1,1] = 5
    X[7,3] = 5
    Field = DataFreq(
        name="field",
        symbol="X",
        axes=[Wavenumber, Freqs],
        values=X,
        unit="m",
    )
    result = Field.get_along("time", "angle")
    time = result["time"]
    assert_array_almost_equal(np.linspace(0,1/f,5,endpoint=False), time)
    angle = result["angle"]
    assert_array_almost_equal(np.linspace(0,2*np.pi,9,endpoint=False), angle)
    ta, at = np.meshgrid(time, angle)
    field_ift = 5*np.cos(2*np.pi*f*ta + 3*at)
    assert_array_almost_equal(field_ift, result["X"])
    
    Field_IFT = Field.freq_to_time()
    assert_array_almost_equal(Field_IFT.get_along("wavenumber", "freqs")["X"], X)
    
    Field_2 = Field_IFT.time_to_freq()
    assert_array_almost_equal(Field_2.get_along("angle", "time")["X"], field_ift)


@pytest.mark.validation
def test_fft2d_period():
    f = 50
    time = np.linspace(0,1/f,10,endpoint=False)
    Time = Data1D(
        name="time",
        unit="s",
        values=time,
        symmetries={"time": {"period":5}}
    )
    angle = np.linspace(0,2*np.pi,20,endpoint=False)
    ta, at = np.meshgrid(time, angle)
    Angle = Data1D(
        name="angle",
        unit="rad",
        values=angle,
        symmetries={"angle": {"period":4}}
    )
    field = 5*np.cos(2*np.pi*f*ta + at)
    # field = 5*np.cos(2*np.pi*f*time)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Angle, Time],
        values=field,
        unit="m",
        symmetries={"angle": {"period":5}, "time": {"period":4}}
    )
    result = Field.get_magnitude_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0,f,2*f]), result["freqs"])
    assert_array_almost_equal(np.array([0,5,0]), result["X"])
    
    result = Field.get_along("wavenumber=[0,10]")
    assert_array_almost_equal(np.array([0,4,8]), result["wavenumber"])
    assert_array_almost_equal(np.array([0,5,0]), result["X"])
    
    result = Field.get_along("freqs=[0,100]", "wavenumber=[0,10]")
    assert_array_almost_equal(np.array([0,f,2*f]), result["freqs"])
    assert_array_almost_equal(np.array([0,4,8]), result["wavenumber"])
    X = np.zeros((3,3))
    X[1,1] = 5
    assert_array_almost_equal(X, result["X"])
    
    Field_FT = Field.time_to_freq()
    assert_array_almost_equal(Field_FT.get_along("angle", "time")["X"], field)

