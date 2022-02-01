import pytest
import numpy as np

from SciDataTool import Data1D


@pytest.mark.validation
def test_filter_meth():
    X = Data1D(
        name="loadcases",
        unit="",
        values=[
            "r=0, radial, stator",
            "r=-2, radial, stator",
            "r=2, radial, stator",
            "r=0, circumferential, stator",
            "r=-2, circumferential, stator",
            "r=2, circumferential, stator",
            "r=0, radial, rotor",
            "r=-2, radial, rotor",
            "r=2, radial, rotor",
            "r=0, circumferential, rotor",
            "r=-2, circumferential, rotor",
            "r=2, circumferential, rotor",
        ],
        is_components=True,
        delimiter=", ",
        filter={
            "wavenumber": ["r=0", "r=-2", "r=2"],
            "direction": ["radial", "circumferential"],
            "application": ["stator", "rotor"],
        },
    )
    indices = X.get_filter(
        filter_dict={
            "wavenumber": ["r=0"],
            "direction": ["radial", "circumferential"],
            "application": ["stator", "rotor"],
        }
    )
    assert indices == [0, 3, 6, 9]
    indices = X.get_filter(
        filter_dict={
            "wavenumber": ["r=0", "r=2"],
            "direction": ["radial"],
            "application": ["stator", "rotor"],
        }
    )
    assert indices == [0, 2, 6, 8]
    indices = X.get_filter(
        filter_dict={
            "wavenumber": ["r=0", "r=2", "r=-2"],
            "direction": ["radial", "circumferential"],
            "application": ["rotor"],
        }
    )
    assert indices == [6, 7, 8, 9, 10, 11]


if __name__ == "__main__":
    test_filter_meth()