import numpy as np
from numpy.testing import assert_array_almost_equal

from SciDataTool.Functions.set_routines import union1d_tol, unique_tol, intersect1d_tol


def test_set_routines():
    """Test to validate set routines"""

    decimal = 4

    tol = 10 ** (-decimal)

    x = np.array([5.236, 8.657, 2, 84.58, 840.663, 2 / 3, 0.66667, np.pi])
    y = np.array([-0.890, 2211.187, 10951.4, 1.028, -0.15607, -4 / 3, 70.21])

    z1, Ia1, Ib1, count1 = unique_tol(
        x,
        tol=tol,
        is_abs_tol=True,
        return_index=True,
        return_inverse=True,
        return_counts=True,
    )
    assert count1[0] == 2
    assert_array_almost_equal(z1[Ib1] - x, 0, decimal=decimal)
    assert_array_almost_equal(z1 - x[Ia1], 0, decimal=decimal)

    z2 = unique_tol(y)
    assert_array_almost_equal(z2 - np.sort(y), 0, decimal=decimal)

    z3, Ia3, Ib3 = union1d_tol(x, y, tol=tol, is_abs_tol=True, return_indices=True)
    assert z3.size == z1.size + z2.size
    assert_array_almost_equal(z3[Ia3] - x, 0, decimal=decimal)
    assert_array_almost_equal(z3[Ib3] - y, 0, decimal=decimal)

    z4 = intersect1d_tol(x, y)
    assert z4.size == 0

    pass


if __name__ == "__main__":

    test_set_routines()
