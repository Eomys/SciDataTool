import pytest
from PySide2.QtWidgets import *

from numpy import linspace, pi
from numpy.random import random
from SciDataTool import DataLinspace, DataTime
from SciDataTool.Functions.Plot import ifft_dict, fft_dict, unit_dict
from SciDataTool.Functions import parser


class TestGUI(object):
    @classmethod
    def setup_class(self):
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

        self.Field = DataTime(
            name="Airgap flux density",
            symbol="B_r",
            unit="T",
            axes=[Time, Angle, Z],
            values=field,
        )

        self.UI = self.Field.plot(is_test=True)

    @pytest.mark.gui
    def check_autorefresh_update(self):
        """Testing that the auto-refresh combobox update the policy correctly"""

        self.UI.c_auto_refresh.setChecked(True)
        assert self.UI.is_auto_refresh == True

        self.UI.c_auto_refresh.setChecked(False)
        assert self.UI.is_auto_refresh == False

    @pytest.mark.gui
    def check_signal(self):
        """Testing that the signals are handled correctly depending on the autorefresh policy"""

        # Setting the policy to true
        self.UI.c_auto_refresh.setChecked(True)
        # Changing axis 1 to send the signal to refresh the plot
        self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(1)
        # making sure that the is_plot_updated is set to True as Autorefresh is activated
        assert self.UI.is_plot_updated == True

        # Setting the policy to true
        self.UI.c_auto_refresh.setChecked(False)
        # Changing axis 1 to send the signal to refresh the plot
        self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(0)
        # making sure that the is_plot_updated is set to False as Autorefresh is desactivated
        assert self.UI.is_plot_updated == False


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing the checkbox
    a.check_autorefresh_update()
    # Verifying the handling of the signals
    a.check_signal()

    print("Done")
