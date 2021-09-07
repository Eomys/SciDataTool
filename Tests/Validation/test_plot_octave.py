import pytest
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import default_rng

from SciDataTool import Data1D, DataTime, DataFreq


@pytest.mark.validation
def test_plot_octave():

    # Load data
    spec_data = np.load("Tests\Data\pinknoise_third_oct.npy")

    # Define axis objects
    frequency = Data1D(
        name="freqs",
        unit="Hz",
        values=spec_data[1, :],
    )

    third_spec = DataFreq(
        name="Pink noise",
        symbol="x",
        axes=[frequency],
        values=spec_data[0, :],
        unit="Pa",
        normalizations={"ref": 2e-5},
    )

    rng = default_rng()
    third_spec_1 = DataFreq(
        name="Signal 2",
        symbol="x",
        axes=[frequency],
        values=rng.standard_normal(28) * 0.006,
        unit="Pa",
        normalizations={"ref": 2e-5},
    )
    third_spec_2 = DataFreq(
        name="Signal 3",
        symbol="x",
        axes=[frequency],
        values=rng.standard_normal(28) * 0.006,
        unit="Pa",
        normalizations={"ref": 2e-5},
    )
    third_spec.plot_2D_Data(
        "freqs", unit="dB", type_plot="octave", data_list=[third_spec_1, third_spec_2]
    )
    plt.show()


if __name__ == "__main__":
    test_plot_octave()