
import pytest
from SciDataTool import DataTime, Data1D, DataLinspace
import numpy as np
from numpy.testing import assert_array_almost_equal


@pytest.mark.validation
def test_period_linspace():
    time = np.linspace(0,10,10,endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=10,
        number=10,
        include_endpoint=False,
    )
    Time_periodic = Time.get_axis_periodic(5)
    field = np.tile(np.arange(50,60,5),5)
    field_periodic = np.arange(50,60,5)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
        symmetries={"time":{"period":5}}
    )
    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])
    
    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0,2,2,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])
    
    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0,2,2,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])


@pytest.mark.validation
def test_period_1d():
    time = np.linspace(0,10,10,endpoint=False)
    Time = Data1D(
        name="time",
        unit="s",
        values=time,
    )
    Time_periodic = Time.get_axis_periodic(5)
    field = np.tile(np.arange(50,60,5),5)
    field_periodic = np.arange(50,60,5)
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
        symmetries={"time":{"period":5}}
    )
    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])
    
    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0,2,2,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])
    
    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0,2,2,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])


@pytest.mark.validation
def test_antiperiod_linspace():
    time = np.linspace(0,16,16,endpoint=False)
    Time = DataLinspace(
        name="time",
        unit="s",
        initial=0,
        final=16,
        number=16,
        include_endpoint=False,
    )
    Time_periodic = Time.get_axis_periodic(4, is_antiperiod=True)
    field_periodic = np.arange(50,70,5)
    field_antisym = np.concatenate((field_periodic, np.negative(field_periodic)))
    field = np.tile(field_antisym, 2)
    
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
        symmetries={"time":{"antiperiod":4}}
    )
    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])
    
    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0,4,4,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])
    
    result = Field.get_along("time[antiperiod]")
    assert_array_almost_equal(np.linspace(0,4,4,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])
    
    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0,8,8,endpoint=False), result["time"])
    assert_array_almost_equal(field_antisym, result["X"])


@pytest.mark.validation
def test_antiperiod_1d():
    time = np.linspace(0,16,16,endpoint=False)
    Time = Data1D(
        name="time",
        unit="s",
        values=time,
    )
    Time_periodic = Time.get_axis_periodic(4, is_antiperiod=True)
    field_periodic = np.arange(50,70,5)
    field = np.concatenate((field_periodic, np.negative(field_periodic)))
    field = np.tile(field, 2)
    
    Field = DataTime(
        name="field",
        symbol="X",
        axes=[Time_periodic],
        values=field_periodic,
        symmetries={"time":{"antiperiod":4}}
    )
    result = Field.get_along("time")
    assert_array_almost_equal(time, result["time"])
    assert_array_almost_equal(field, result["X"])
    
    result = Field.get_along("time[smallestperiod]")
    assert_array_almost_equal(np.linspace(0,4,4,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])
    
    result = Field.get_along("time[antiperiod]")
    assert_array_almost_equal(np.linspace(0,4,4,endpoint=False), result["time"])
    assert_array_almost_equal(field_periodic, result["X"])
    
    result = Field.get_along("time[oneperiod]")
    assert_array_almost_equal(np.linspace(0,8,8,endpoint=False), result["time"])
    assert_array_almost_equal(field_antisym, result["X"])
