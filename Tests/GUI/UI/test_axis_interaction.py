import pytest
from PySide2 import QtWidgets
import sys
from Tests.GUI import Field
from SciDataTool.Functions.Plot import fft_dict, unit_dict


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
    def test_check_axis_removal(self):
        """Test that make sure that when an axis is selected in axis 1 then it is not in axis 2"""
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1
        axis_2 = self.UI.w_plot_manager.w_axis_manager.w_axis_2

        for index_axis_1 in range(axis_1.c_axis.count()):

            axis_1.c_axis.setCurrentIndex(index_axis_1)
            for index_axis_2 in range(axis_2.c_axis.count()):
                axis_2.c_axis.setCurrentIndex(index_axis_2)
                assert axis_1.c_axis.currentText() != axis_2.c_axis.currentText()

    @pytest.mark.gui
    def test_check_filter(self):
        """Checking that when Filter is selected, then the button is enabled. Otherwise it must be disabled."""
        # Making sure that the two axis have their default value (time and None)
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1
        axis_2 = self.UI.w_plot_manager.w_axis_manager.w_axis_2

        axis_1.c_axis.setCurrentIndex(0)
        axis_2.c_axis.setCurrentIndex(0)

        for index in range(axis_1.c_action.count()):
            axis_1.c_action.setCurrentIndex(index)

            if axis_1.c_action.currentText() == "Filter":
                assert axis_1.b_filter.isEnabled()
            else:
                assert not axis_1.b_filter.isEnabled()

    @pytest.mark.gui
    def test_check_ope_available(self):
        """Test to make sure that the action available for each axis is correct"""
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1

        for index_axis in range(axis_1.c_axis.count()):
            axis_1.c_axis.setCurrentIndex(index_axis)

            action_list = list()
            for index_ope in range(axis_1.c_action.count()):
                axis_1.c_action.setCurrentIndex(index_ope)
                action_list.append(axis_1.c_action.currentText())

            assert "None" in action_list
            if axis_1.axes_list_obj[
                axis_1.axes_list.index(axis_1.axis_selected)
            ].is_components:
                assert "Filter" in action_list
            else:
                assert "Filter" not in action_list

            if axis_1.c_axis.currentText() in fft_dict:
                assert "FFT" in action_list
            else:
                assert "FFT" not in action_list

    @pytest.mark.gui
    def test_check_ope_sync(self):
        """Checking that when FFT or '' is selected in axis 1 then the action of the axis 2 is synchronized to be the same"""
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1
        axis_2 = self.UI.w_plot_manager.w_axis_manager.w_axis_2

        # Making sure that two axis where we can apply a fft are selected
        # selecting time
        axis_1.c_axis.setCurrentIndex(0)
        # selecting angle
        axis_2.c_axis.setCurrentIndex(1)

        for index in range(axis_1.c_action.count()):
            axis_1.c_action.setCurrentIndex(index)

            if (
                axis_1.c_action.currentText() == ""
                or axis_1.c_action.currentText() == "FFT"
            ):
                assert axis_1.c_action.currentText() == axis_2.c_action.currentText()

        for index in range(axis_2.c_action.count()):
            axis_2.c_action.setCurrentIndex(index)

            if (
                axis_2.c_action.currentText() == ""
                or axis_2.c_action.currentText() == "FFT"
            ):
                assert axis_1.c_action.currentText() == axis_2.c_action.currentText()

        # Checking what happened on axis2 if axis1 already had an action selected
        # selecting time on axis 1
        axis_1.c_axis.setCurrentIndex(0)
        # selecting None on axis 2
        axis_2.c_axis.setCurrentIndex(0)
        # selecting fft for axis 1
        axis_1.c_action.setCurrentIndex(1)
        # selecting angle on axis 2
        axis_2.c_axis.setCurrentIndex(1)
        # Making sure that FFT is selected on second axis
        assert axis_2.c_action.currentIndex() == axis_1.c_action.currentIndex()

    @pytest.mark.gui
    def test_check_unit_available(self):
        """Test to make sure that the unit available are adapting correctly depending on the combination of axis and action"""
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1

        # Gathering all the units available for a specific combination and we compare it with the reference with is unit_dict
        for index_axis in range(axis_1.c_axis.count()):
            axis_1.c_axis.setCurrentIndex(index_axis)
            for index_ope in range(axis_1.c_action.count()):
                axis_1.c_action.setCurrentIndex(index_ope)

                unit_list = list()
                for index_unit in range(axis_1.c_unit.count()):
                    unit_list.append(axis_1.c_unit.itemText(index_unit))

                if isinstance(unit_dict[axis_1.get_axis_selected()], list):
                    assert unit_list == unit_dict[axis_1.get_axis_selected()]
                else:
                    assert unit_list[0] == unit_dict[axis_1.get_axis_selected()]


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing the removal of axis1 in axis2
    a.test_check_axis_removal()
    # Checking the update of the action according to the choice of the axis selected
    a.test_check_ope_available()
    # Checking the update of the unit according to the action and the axis selected
    a.test_check_unit_available()
    # Checking the update of the FFT action of axis2 if selected in axis1
    a.test_check_ope_sync()
    # Checking the interaction with filter button
    a.test_check_filter()

    print("Done")
