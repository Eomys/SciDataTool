import pytest
from PySide2.QtWidgets import *

from Tests.GUI import Field
from SciDataTool.Functions.Plot import fft_dict, unit_dict


class TestGUI(object):
    @classmethod
    def setup_class(self):
        self.UI = Field.plot(is_test=True)

    @pytest.mark.gui
    def check_axis_removal(self):
        """Test that make sure that when an axis is selected in axis 1 then it is not in axis 2"""
        for index_axis_1 in range(
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.count()
        ):

            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(
                index_axis_1
            )

            for index_axis_2 in range(
                self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.count()
            ):
                self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(
                    index_axis_2
                )
                assert (
                    self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.currentText()
                    != self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.currentText()
                )

    @pytest.mark.gui
    def check_filter(self):
        """Checking that when Filter is selected, then the button is enabled. Otherwise it must be disabled."""
        # Making sure that the two axis have their default value (time and None)
        self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(0)
        self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(0)

        for index in range(
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.count()
        ):
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.setCurrentIndex(
                index
            )

            if (
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.currentText()
                == "Filter"
            ):
                assert (
                    self.UI.w_plot_manager.w_axis_manager.w_axis_1.b_filter.isEnabled()
                )
            else:
                assert (
                    not self.UI.w_plot_manager.w_axis_manager.w_axis_1.b_filter.isEnabled()
                )

    @pytest.mark.gui
    def check_ope_available(self):
        """Test to make sure that the operation available for each axis is correct"""

        for index_axis in range(
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.count()
        ):
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(
                index_axis
            )

            operation_list = list()
            for index_ope in range(
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.count()
            ):
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.setCurrentIndex(
                    index_ope
                )
                operation_list.append(
                    self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.currentText()
                )

            assert "None" in operation_list
            assert "Filter" in operation_list

            if (
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.currentText()
                in fft_dict
            ):
                assert "FFT" in operation_list

    @pytest.mark.gui
    def check_ope_sync(self):
        """Checking that when FFT or '' is selected in axis 1 then the operation of the axis 2 is synchronized to be the same"""

        # Making sure that two axis where we can apply a fft are selected
        # selecting time
        self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(0)
        # selecting angle
        self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(1)

        for index in range(
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.count()
        ):
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.setCurrentIndex(
                index
            )

            if (
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.currentText()
                == ""
                or self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.currentText()
                == "FFT"
            ):
                assert (
                    self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.currentText()
                    == self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_action.currentText()
                )

        for index in range(
            self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_action.count()
        ):
            self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_action.setCurrentIndex(
                index
            )

            if (
                self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_action.currentText()
                == ""
                or self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_action.currentText()
                == "FFT"
            ):
                assert (
                    self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.currentText()
                    == self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_action.currentText()
                )

    @pytest.mark.gui
    def check_unit_available(self):
        """Test to make sure that the unit available are adapting correctly depending on the combination of axis and operation"""

        # Gathering all the units available for a specific combination and we compare it with the reference with is unit_dict
        for index_axis in range(
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.count()
        ):
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(
                index_axis
            )
            for index_ope in range(
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.count()
            ):
                self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_action.setCurrentIndex(
                    index_ope
                )

                unit_list = list()
                for index_unit in range(
                    self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_unit.count()
                ):
                    self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_unit.setCurrentIndex(
                        index_unit
                    )
                    unit_list.append(
                        self.UI.w_plot_manager.w_axis_manager.w_axis_1.c_unit.currentText()
                    )

                assert (
                    unit_list
                    == unit_dict[
                        self.UI.w_plot_manager.w_axis_manager.w_axis_1.get_axis_selected()
                    ]
                )


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing the removal of axis1 in axis2
    a.check_axis_removal()
    # Checking the update of the operation according to the choice of the axis selected
    a.check_ope_available()
    # Checking the update of the unit according to the operation and the axis selected
    a.check_unit_available()
    # Checking the update of the FFT operation of axis2 if selected in axis1
    a.check_ope_sync()
    # Checking the interaction with filter button
    a.check_filter()

    print("Done")
