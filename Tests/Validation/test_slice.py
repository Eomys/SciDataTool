import pytest
from SciDataTool import DataLinspace, DataTime
from numpy import meshgrid
from numpy.testing import assert_array_almost_equal


@pytest.mark.validation
# @pytest.mark.DEV
def test_slice():
    """Test slicing"""
    X = DataLinspace(name="X", unit="m", initial=0, final=10, number=11)
    Y = DataLinspace(name="Y", unit="m", initial=0, final=100, number=11)
    y, x = meshgrid(Y.get_values(), X.get_values())
    field = x + y
    Field = DataTime(name="Example field", symbol="Z", axes=[X, Y], values=field)

    # Extract data by axis value
    # 'X=1'
    result = Field.get_along("X=1", "Y")
    assert_array_almost_equal(field[1, :], result["Z"])

    # 'X=[0, 1]'
    result = Field.get_along("X=[0, 1]", "Y")
    expected = field[0:2, :]
    assert_array_almost_equal(expected, result["Z"])

    # 'X<2' #TODO result in an error
    result = Field.get_along("X<2", "Y")
    expected = field[0:2, :]
    # assert_array_almost_equal(expected, result["Z"])

    # Extract data by operator
    # mean value 'X=mean'
    result = Field.get_along("X=mean", "Y")
    expected = field.mean(axis=0)
    assert_array_almost_equal(expected, result["Z"])

    # sum 'X=sum'
    result = Field.get_along("X=sum", "Y")
    expected = field.sum(axis=0)
    assert_array_almost_equal(expected, result["Z"])

    # rms value 'X=rms'
    result = Field.get_along("X=rms", "Y")
    expected = (field ** 2).mean(axis=0) ** (1 / 2)
    assert_array_almost_equal(expected, result["Z"])

    # Extract data by indices
    result = Field.get_along("X[1:5]", "Y[2:8]")
    expected = field[1:5, 2:8]
    assert_array_almost_equal(expected, result["Z"])


if __name__ == "__main__":
    test_slice()
