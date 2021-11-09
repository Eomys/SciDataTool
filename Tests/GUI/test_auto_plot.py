from types import FrameType
import pytest
from PySide2.QtWidgets import *

from numpy import linspace, pi
from numpy.random import random
from SciDataTool import DataLinspace, DataTime
from SciDataTool.Functions.Plot import ifft_dict, fft_dict, unit_dict
from SciDataTool.Functions import parser


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        f = 50
        Nt_tot = 16
        Na_tot = 20

        Time = DataLinspace(
            name="time", unit="s", initial=0, final=1 / (2 * f), number=Nt_tot
        )
        Angle = DataLinspace(
            name="angle", unit="rad", initial=0, final=2 * pi, number=Na_tot
        )
        Z = DataLinspace(name="z", unit="m", initial=-1, final=1, number=3)

        field = random((Nt_tot, Na_tot, 3))

        cls.Field = DataTime(
            name="Airgap flux density",
            symbol="B_r",
            unit="T",
            axes=[Time, Angle, Z],
            values=field,
        )

    @classmethod
    def teardown_class(cls):
        """Exit the app after the test"""

        cls.app.quit()

    @pytest.mark.gui
    def check_axis(self):
        """Test to make sure that the auto-plot functions for its axes"""

        # Checking case where everything is given to the autoplot
        self.app, self.UI = self.Field.plot(
            "time", "angle{°}", "z[2]", is_test=True, unit="T", zmax="50"
        )

        # Checking that the axis are correct, that the slice are correct, datarange is correct

        # Check if one axis is given and full dict
        self.app, self.UI = self.Field.plot("time", is_test=True, unit="T", zmax="50")
        # Checking that the axis are correct, that the default slice are correct, datarange is correct

        # Checking case where the dict is not given to the autoplot
        self.app, self.UI = self.Field.plot("time", "angle{°}", "z[2]", is_test=True)
        # Checking that the axis are correct, that the slice are correct, default datarange is correct

        # Checking case where different axis are given (transformation necessary)
        self.app, self.UI = self.Field.plot(
            "freqs", "wavenumber", "z[2]", is_test=True, unit="T", zmax="50"
        )

        # Checking case with all of the operation
        self.app, self.UI = self.Field.plot(
            "time", "angle{°}", "z[2]", is_test=True, unit="T", zmax="50"
        )

    @pytest.mark.gui
    def check_spec_axis(self):
        """Test to make sure that the auto-plot functions for other axes (fft axes)"""


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Checking the auto setup of the axes
    a.check_axis()
    # Checking the auto setup of data_selection

    # Checking the auto setup of WDataRange

    a.teardown_class()
    print("Done")
