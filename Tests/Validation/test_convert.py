import pytest
from SciDataTool import DataTime, DataLinspace
import numpy as np
from numpy.testing import assert_array_almost_equal


@pytest.mark.validation
def test_units():
    time = np.linspace(0,10,10,endpoint=False)
    angle = np.linspace(0,2*np.pi,20,endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=10,
        number=10,
        include_endpoint=False,
    )
    Angle = DataLinspace(
        name="angle",
        unit="rad",
        initial=0,
        final=2*np.pi,
        number=20,
        include_endpoint=False,
    )
    field = np.ones((10,20))
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time, Angle],
        values=field,
        unit="m/s2",
    )
    result = Field.get_along("time{ms}", unit="km/h2")
    assert_array_almost_equal(1e3*time, result["time"])
    assert_array_almost_equal(12960*field[:,0], result["X"])
    
    result = Field.get_along("angle{°}", unit="dm/ms2")
    assert_array_almost_equal(180/np.pi*angle, result["angle"])
    assert_array_almost_equal(1e-5*field[0,:], result["X"])


@pytest.mark.validation
def test_norm():
    time = np.linspace(0,10,10,endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=10,
        number=10,
        include_endpoint=False,
        normalizations={"elec_order": 7}
    )
    field = np.cos(2*np.pi*100*time)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time],
        values=field,
        unit="m/s2",
        normalizations={"ref": 0.2}
    )
    result = Field.get_along("freqs->elec_order=[0,100]", is_norm=True)
    assert_array_almost_equal(1/(7*10), result["freqs"][1])
    assert_array_almost_equal(1/0.2, result["X"][0])


