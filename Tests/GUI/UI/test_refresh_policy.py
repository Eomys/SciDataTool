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
    def test_check_autorefresh_update(self):
        """Testing that the auto-refresh combobox update the policy correctly"""

        self.UI.is_auto_refresh.setChecked(True)
        assert self.UI.auto_refresh == True

        self.UI.is_auto_refresh.setChecked(False)
        assert self.UI.auto_refresh == False

    @pytest.mark.gui
    def test_check_signal(self):
        """Testing that the signals are handled correctly depending on the autorefresh policy"""

        # Setting the policy to true
        self.UI.is_auto_refresh.setChecked(True)
        # Changing axis 1 to send the signal to refresh the plot
        self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(1)
        # making sure that the is_plot_updated is set to True as Autorefresh is activated
        assert self.UI.is_plot_updated == True

        # Setting the policy to true
        self.UI.is_auto_refresh.setChecked(False)
        # Changing axis 1 to send the signal to refresh the plot
        self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(0)
        # making sure that the is_plot_updated is set to False as Autorefresh is desactivated
        assert self.UI.is_plot_updated == False

    @pytest.mark.gui
    def test_check_b_refresh_auto_refresh(self):
        """Testing that the refresh button is enabled and disabled according to the action on the UI"""

        # Testing that when auto-refresh is checked, then the refresh button is disabled
        self.UI.is_auto_refresh.setChecked(True)
        assert self.UI.b_refresh.isEnabled() == False

        # Testing that when auto-refresh is unchecked, then the refresh button is enabled
        self.UI.is_auto_refresh.setChecked(False)
        assert self.UI.b_refresh.isEnabled() == True

    @pytest.mark.gui
    def test_check_b_refresh_auto(self):
        "Testing that when a plot is updated, then the refresh button is disabled and that we enable it once the UI is modified"

        # After updating the plot, the button should be disabled
        self.UI.update_plot()
        assert self.UI.b_refresh.isEnabled() == False

        # After modifying the UI, the button shoud be enabled
        self.UI.w_plot_manager.updatePlot.emit()
        assert self.UI.b_refresh.isEnabled() == True


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing the checkbox
    a.test_check_autorefresh_update()
    # Verifying the handling of the signals
    a.test_check_signal()
    # Testing that we disable/enable b_refresh according to is_auto_refresh (checkBox)
    a.test_check_b_refresh_auto_refresh()
    # Testing that the button is disabled after the plot is updated and enabled after changing the UI
    a.test_check_b_refresh_auto

    print("Done")
