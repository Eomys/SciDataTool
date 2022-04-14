import pytest
from PySide2 import QtWidgets
import sys
from SciDataTool import DataTime, DataLinspace
from numpy import pi
from numpy.random import random

f_t_test_list = list()

f_t_test_list.append(
    {
        "axis": ["time", "angle"],
        "is_create_appli": False,
        "is_show_fig": False,
        "frozen_type": 1,
    }
)  # Testing plot which is soft frozen

f_t_test_list.append(
    {
        "axis": ["time", "angle"],
        "is_create_appli": False,
        "is_show_fig": False,
        "frozen_type": 2,
    }
)  # Testing plot which is hard frozen

f_t_test_list.append(
    {
        "axis": ["time", "angle"],
        "is_create_appli": False,
        "is_show_fig": False,
        "frozen_type": 3,
    }
)  # Testing plot which is very hard frozen


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

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

    @pytest.mark.gui
    @pytest.mark.parametrize("test_dict", f_t_test_list)
    def test_check_frozen_type(self, test_dict):
        """Test to make sure that the auto-plot works as intended"""

        # Launching the auto plot with info from the dict
        self.UI = self.Field.plot(
            test_dict["axis"][0],
            test_dict["axis"][1],
            is_create_appli=test_dict["is_create_appli"],
            is_show_fig=test_dict["is_show_fig"],
            frozen_type=test_dict["frozen_type"],
        )

        # Checking that we fill the combobox with the requested axis if the frozen type is "soft" (==1)
        if test_dict["frozen_type"] == 1:
            assert (
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.get_axes_name()
                == test_dict["axis"]
            )
            assert (
                self.UI.w_plot_manager.w_axis_manager.w_axis_2.get_axes_name()
                == test_dict["axis"]
            )

        # Checking that we disable the combobox if the frozen type chosen is "hard" (==2)
        elif test_dict["frozen_type"] == 2:
            assert not self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.isEnabled()
            assert not self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.isEnabled()

        # Checking that we disable the axes and the operations if the frozen type chosen is "very hard" (3)
        elif test_dict["frozen_type"] == 3:
            assert not self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.isEnabled()
            assert not self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.isEnabled()

            for w_op in self.UI.w_plot_manager.w_axis_manager.w_slice_op:
                assert not w_op.c_operation.isEnabled()
                assert not w_op.lf_value.isEnabled()
                assert not w_op.slider.isEnabled()


if __name__ == "__main__":

    for ii, f_t_test in enumerate(f_t_test_list):
        a = TestGUI()
        a.setup_class()

        # Testing that the checkbox are disabled if there is only one item in them
        a.test_check_frozen_type(f_t_test)

        print("Test n°" + str(ii) + " done")
