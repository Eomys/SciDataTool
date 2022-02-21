import pytest
from PySide2 import QtWidgets
import sys
from numpy import ones
from SciDataTool import DataTime, DataLinspace
from numpy import pi


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

        X = DataLinspace(name="time", unit="s", initial=0, final=10, number=11)
        Y = DataLinspace(
            name="angle",
            unit="rad",
            initial=0,
            final=2 * pi,
            number=21,
            is_overlay=True,
            is_components=True,
        )
        field_2d = ones((11, 21))
        for i in range(11):
            field_2d[i] *= i

        cls.Field = DataTime(
            name="Airgap flux density",
            symbol="B_r",
            unit="T",
            axes=[X, Y],
            values=field_2d,
        )

        cls.UI = cls.Field.plot(is_show_fig=False, is_create_appli=False)

    @pytest.mark.gui
    def test_check_combobox(self):
        """Testing that the combobox is disabled if there is only one item"""

        # As we only have one axis then the combobox is disabled
        assert (
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.isEnabled() == False
        )

    def test_check_axis_2(self):
        """Testing that the second WAxisSelector is hidden as the second axis has is_overlay = True"""

        assert self.UI.w_plot_manager.w_axis_manager.w_axis_2.isHidden() == True

    def test_check_slice_op(self):
        """Testing that the is_overlay axis generated a WSliceOperator widget"""

        axis_slice_op = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0].axis
        overlay_axis = self.Field.get_axes()[1]

        assert axis_slice_op.name == overlay_axis.name


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing that the checkbox are disabled if there is only one item in them
    a.test_check_combobox()

    # Testing that axis 2 is hidden
    a.test_check_axis_2()

    # Testing that the second axis is a WSliceOperator widget
    a.test_check_slice_op()

    print("Done")
