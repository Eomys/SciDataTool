import pytest
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
import sys
from Tests.GUI import Field_filter
from SciDataTool.GUI.WFilter.WFilter import WFilter


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

        cls.UI = Field_filter.plot(
            "time", "loadcases[]", is_show_fig=False, is_create_appli=False
        )

    @pytest.mark.gui
    def test_check_filter_buttons(self):
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1
        slice_op = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0]
        assert not slice_op.b_action.isHidden()

    @pytest.mark.gui
    def test_check_filter_table_init(self):
        # Check that filter table initializes correctly
        self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].b_action.clicked.emit()
        wfilter = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].current_dialog
        assert isinstance(wfilter, WFilter)
        assert wfilter.indices == [i for i in range(12)]
        wfilter.b_Ok.clicked.emit()
        assert wfilter.indices == [i for i in range(12)]
        assert self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].indices == [
            i for i in range(12)
        ]
        # Select 3 indices and check table initialization
        self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].indices = [0, 2, 5]
        self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].b_action.clicked.emit()
        wfilter = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].current_dialog
        assert isinstance(wfilter, WFilter)
        assert wfilter.indices == [0, 2, 5]

    @pytest.mark.gui
    def test_check_filter_table_manip(self):
        self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].b_action.clicked.emit()
        wfilter = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].current_dialog
        assert isinstance(wfilter, WFilter)
        assert wfilter.indices == [0, 2, 5]
        # Uncheck one line and check indices
        wfilter.tab_indices.model().data(
            wfilter.tab_indices.model().index(
                2, wfilter.tab_indices.model().columnCount() - 1
            )
        ).setCheckState(Qt.CheckState(False))
        wfilter.b_Ok.clicked.emit()
        assert wfilter.indices == [0, 5]
        # Sort by first column and check indices
        self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].b_action.clicked.emit()
        wfilter = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].current_dialog
        assert isinstance(wfilter, WFilter)
        wfilter.tab_indices.model().sort(0, Qt.AscendingOrder)
        wfilter.b_Ok.clicked.emit()
        assert list(set(wfilter.indices)) == [0, 5]


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()
    # a.test_check_filter_buttons()
    # a.test_check_filter_table_init()
    a.test_check_filter_table_manip()

    print("Done")
