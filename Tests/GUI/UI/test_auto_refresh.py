import pytest
from PySide2 import QtWidgets
from Tests.GUI import Field
import sys


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

        cls.UI = Field.plot(is_show_fig=False, is_create_appli=False)

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
        self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(1)
        # making sure that the is_plot_updated is set to True as Autorefresh is activated
        assert self.UI.is_plot_updated == True

        # Setting the policy to true
        self.UI.c_auto_refresh.setChecked(False)
        # Changing axis 1 to send the signal to refresh the plot
        self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(0)
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
