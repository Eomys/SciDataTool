import pytest
from PySide2.QtWidgets import *

from Tests.GUI import Field
from Tests import save_gui_path
from os.path import join, isfile


class TestGUI(object):
    @classmethod
    def setup_class(self):
        self.UI = Field.plot(is_test=True)

    @pytest.mark.gui
    def check_export_path(self):
        """Testing that the export function save a file at the right place by checking the path"""

        # Exporting the file
        self.UI.w_plot_manager.export(save_gui_path)

        # Building the path where the file should be stored
        param_list = [
            *self.UI.w_plot_manager.w_axis_manager.get_axes_selected(),
            *self.UI.w_plot_manager.w_axis_manager.get_operation_selected(),
        ]

        file_name = (
            "plot_"
            + self.UI.w_plot_manager.data.symbol
            + "_"
            + "_".join(param_list)
            + ".csv"
        )

        # Testing that the file exists
        assert isfile(join(save_gui_path, file_name))


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing that the file exists in the right folder
    a.check_export_path()

    print("Done")
