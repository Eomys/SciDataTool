
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
    field = 3*np.cos(2*np.pi*f*ta + 3*at)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Angle, Time],
        values=field,
        unit="m",
    )
    result = Field.get_along("freqs=[0,100]")
    assert_array_almost_equal(np.array([0,f,2*f]), result["freqs"])
    assert_array_almost_equal(np.array([0,3,0]), result["X"])
    
    result = Field.get_along("wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0,1,2,3,4]), result["wavenumber"])
    assert_array_almost_equal(np.array([0,0,0,3,0]), result["X"])
    
    result = Field.get_along("freqs=[0,100]", "wavenumber=[0,4]")
    assert_array_almost_equal(np.array([0,f,2*f]), result["freqs"])
    assert_array_almost_equal(np.array([0,1,2,3,4]), result["wavenumber"])
    X = np.zeros((5,3))
    X[3,1] = 3
    assert_array_almost_equal(X, result["X"])


@pytest.mark.validation
def test_ifft1d():    
    f = 50
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
    field = 3*np.cos(2*np.pi*f*time) + 5*np.sin(2*np.pi*f*time)
    assert_array_almost_equal(field, result["X"])