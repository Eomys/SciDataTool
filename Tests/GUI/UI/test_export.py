import pytest
from PySide2 import QtWidgets
import sys
from Tests.GUI import Field
from Tests import save_gui_path
from os.path import join, isfile


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
    def test_check_export_path(self):
        """Testing that the export function save a file at the right place by checking the path"""

        # Exporting the file
        self.UI.w_plot_manager.export(save_gui_path)

        # Building the path where the file should be stored
        param_list = [
            *self.UI.w_plot_manager.w_axis_manager.get_axes_selected(),
            *self.UI.w_plot_manager.w_axis_manager.get_operation_selected(),
        ]

        file_name = (
            (self.UI.w_plot_manager.data.symbol + "_" + "_".join(param_list))
            .replace("{", "")
            .replace("}", "")
            .replace(".", ",")
        ) + ".csv"

        # Testing that the file exists
        assert isfile(join(save_gui_path, file_name))


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing that the file exists in the right folder
    a.test_check_export_path()

    print("Done")
