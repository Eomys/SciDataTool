import pytest
from PySide2.QtWidgets import *

from numpy import linspace, pi
from numpy.random import random
from SciDataTool import DataLinspace, DataTime
from SciDataTool.Functions.Plot import ifft_dict, fft_dict, unit_dict
from SciDataTool.Functions import parser


class TestGUI(object):
    @classmethod
    def setup_class(cls):
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

        cls.app, cls.UI = cls.Field.plot(is_test=True)

    @classmethod
    def teardown_class(cls):
        """Exit the app after the test"""

        cls.app.quit()

    @pytest.mark.gui
    def axis_interaction(self):
        """Test that will make sure that the interaction within an axis and between them, are working correctly"""

        # Testing the removal of axis1 in axis2
        self.check_axis_removal()
        # Checking the update of the operation according to the choice of the axis selected
        self.check_ope_available()
        # Checking the update of the unit according to the operation and the axis selected
        self.check_unit_available()
        # Checking the update of the FFT operation of axis2 if selected in axis1
        self.check_ope_sync()
        # Checking the interaction with filter button
        self.check_filter()

    def check_axis_removal(self):
        """Test that make sure that when an axis is selected in axis 1 then it is not in axis 2"""
        for index_axis_1 in range(self.UI.w_axis_manager.w_axis_1.c_axis.count()):

            self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(index_axis_1)

            for index_axis_2 in range(self.UI.w_axis_manager.w_axis_2.c_axis.count()):
                self.UI.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(index_axis_2)
                assert (
                    self.UI.w_axis_manager.w_axis_1.c_axis.currentText()
                    != self.UI.w_axis_manager.w_axis_2.c_axis.currentText()
                )

    def check_filter(self):
        """Checking that when Filter is selected, then the button is enabled. Otherwise it must be disabled."""
        # Making sure that the two axis have their default value (time and None)
        self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(0)
        self.UI.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(0)

        for index in range(self.UI.w_axis_manager.w_axis_1.c_operation.count()):
            self.UI.w_axis_manager.w_axis_1.c_operation.setCurrentIndex(index)

            if self.UI.w_axis_manager.w_axis_1.c_operation.currentText() == "Filter":
                assert self.UI.w_axis_manager.w_axis_1.b_filter.isEnabled()
            else:
                assert not self.UI.w_axis_manager.w_axis_1.b_filter.isEnabled()

    def check_ope_available(self):
        """Test to make sure that the operation available for each axis is correct"""

        for index_axis in range(self.UI.w_axis_manager.w_axis_1.c_axis.count()):
            self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(index_axis)

            operation_list = list()
            for index_ope in range(self.UI.w_axis_manager.w_axis_1.c_operation.count()):
                self.UI.w_axis_manager.w_axis_1.c_operation.setCurrentIndex(index_ope)
                operation_list.append(
                    self.UI.w_axis_manager.w_axis_1.c_operation.currentText()
                )

            assert "" in operation_list
            assert "Filter" in operation_list

            if self.UI.w_axis_manager.w_axis_1.c_axis.currentText() in fft_dict:
                assert "FFT" in operation_list

    def check_ope_sync(self):
        """Checking that when FFT or '' is selected in axis 1 then the operation of the axis 2 is synchronized to be the same"""

        # Making sure that two axis where we can apply a fft are selected
        # selecting time
        self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(0)
        # selecting angle
        self.UI.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(1)

        for index in range(self.UI.w_axis_manager.w_axis_1.c_operation.count()):
            self.UI.w_axis_manager.w_axis_1.c_operation.setCurrentIndex(index)

            if (
                self.UI.w_axis_manager.w_axis_1.c_operation.currentText() == ""
                or self.UI.w_axis_manager.w_axis_1.c_operation.currentText() == "FFT"
            ):
                assert (
                    self.UI.w_axis_manager.w_axis_1.c_operation.currentText()
                    == self.UI.w_axis_manager.w_axis_2.c_operation.currentText()
                )

    def check_unit_available(self):
        """Test to make sure that the unit available are adapting correctly depending on the combination of axis and operation"""

        # Gathering all the units available for a specific combination and we compare it with the reference with is unit_dict
        for index_axis in range(self.UI.w_axis_manager.w_axis_1.c_axis.count()):
            self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(index_axis)
            for index_ope in range(self.UI.w_axis_manager.w_axis_1.c_operation.count()):
                self.UI.w_axis_manager.w_axis_1.c_operation.setCurrentIndex(index_ope)

                unit_list = list()
                for index_unit in range(self.UI.w_axis_manager.w_axis_1.c_unit.count()):
                    self.UI.w_axis_manager.w_axis_1.c_unit.setCurrentIndex(index_unit)
                    unit_list.append(
                        self.UI.w_axis_manager.w_axis_1.c_unit.currentText()
                    )

                assert (
                    unit_list
                    == unit_dict[
                        self.UI.w_axis_manager.w_axis_1.get_current_axis_selected()
                    ]
                )


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()
    a.axis_interaction()
    a.teardown_class()
    print("Done")
