import pytest
from PySide2.QtWidgets import *

from numpy import linspace, pi
from numpy.random import random
from SciDataTool import DataLinspace, DataTime
from SciDataTool.Functions.Plot import ifft_dict, fft_dict, unit_dict, axes_dict
from SciDataTool.Functions import parser
from SciDataTool.GUI.WDataExtractor.WDataExtractor import type_extraction_dict


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
    def string_gen(self):
        """Test that will make sure that the strings are generated the right way and that they are following the changes in the UI"""

        # Checking that the string generated for the axes are correct
        self.check_axes_strings()
        # Making sure that the string is updated according to the change of the UI (FFT to '' for ex)
        self.check_axis_updated()
        # When modifying WDataRange, making sure that the string is updated correctly
        self.check_range_updated()
        # When modifying DataSelection, making sure that the string is updated correctly (slice to sum for ex)
        self.check_string_dataselection()

    def check_axes_strings(self):
        "Testing that the string generated corresponds to the info given by the user"

        for index_axis_1 in range(self.UI.w_axis_manager.w_axis_1.c_axis.count()):
            self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(index_axis_1)
            for index_axis_2 in range(self.UI.w_axis_manager.w_axis_2.c_axis.count()):
                self.UI.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(index_axis_2)

                axes_selected = parser.read_input_strings(
                    self.UI.w_axis_manager.get_axes_selected(), axis_data=None
                )

                # Checking that the axis string is correct
                if axes_selected[0].name in ifft_dict:
                    assert (
                        ifft_dict[axes_selected[0].name]
                        == self.UI.w_axis_manager.w_axis_1.c_axis.currentText()
                        and self.UI.w_axis_manager.w_axis_1.c_operation.currentText()
                        == "FFT"
                    )

                elif axes_selected[0].name in axes_dict:
                    assert (
                        axes_dict[axes_selected[0].name]
                        == self.UI.w_axis_manager.w_axis_1.c_axis.currentText()
                    )

                else:
                    assert (
                        axes_selected[0].name
                        == self.UI.w_axis_manager.w_axis_1.c_axis.currentText()
                    )
                # Checking that the unit in the string is correct
                assert (
                    axes_selected[0].unit
                    == self.UI.w_axis_manager.w_axis_1.c_unit.currentText()
                )

                # if an axis is selected on axis 2 the we check its string as well
                if len(axes_selected) == 2:

                    # Checking that the axis string is correct
                    if axes_selected[1].name in ifft_dict:
                        assert (
                            ifft_dict[axes_selected[1].name]
                            == self.UI.w_axis_manager.w_axis_2.c_axis.currentText()
                            and self.UI.w_axis_manager.w_axis_2.c_operation.currentText()
                            == "FFT"
                        )

                    elif axes_selected[1].name in axes_dict:
                        assert (
                            axes_dict[axes_selected[1].name]
                            == self.UI.w_axis_manager.w_axis_2.c_axis.currentText()
                        )

                    else:
                        assert (
                            axes_selected[1].name
                            == self.UI.w_axis_manager.w_axis_2.c_axis.currentText()
                        )
                    # Checking that the unit in the string is correct
                    assert (
                        axes_selected[1].unit
                        == self.UI.w_axis_manager.w_axis_2.c_unit.currentText()
                    )

                # Checking that the axes in DataSelection are not those selected
                action_selected = parser.read_input_strings(
                    self.UI.w_axis_manager.get_operation_selected(), axis_data=None
                )

                if len(action_selected) == 1:
                    assert (
                        action_selected[0].name != axes_selected[0].name
                        and action_selected[0].name != axes_selected[1].name
                    )

                if len(action_selected) > 1:

                    for action in action_selected:
                        assert action.name != axes_selected[0].name

    def check_axis_updated(self):
        """Test to make sure that when we switch from time to frequency (or from angle to wavenb), the string is updated correclty"""

        for index_axis in range(self.UI.w_axis_manager.w_axis_1.c_axis.count()):
            self.UI.w_axis_manager.w_axis_1.c_axis.setCurrentIndex(index_axis)
            axes = list()

            if self.UI.w_axis_manager.w_axis_1.get_current_axis_selected() in fft_dict:
                # Recovering the string when '' is selected
                self.UI.w_axis_manager.w_axis_1.c_operation.setCurrentIndex(0)
                axes.append(self.UI.w_axis_manager.w_axis_1.get_axis_unit_selected())
                # Recovering the string when 'FFT' is selected
                self.UI.w_axis_manager.w_axis_1.c_operation.setCurrentIndex(1)
                axes.append(self.UI.w_axis_manager.w_axis_1.get_axis_unit_selected())
                # Processing the string to compare them
                axes_parsed = parser.read_input_strings(axes, axis_data=None)

                assert axes_parsed[1].name == fft_dict[axes_parsed[0].name]

    def check_range_updated(self):
        """Testing how WDataRange string are generated after updating the widget"""

        # Test 1 : Making sure that min and max are updated
        new_min = 15.0
        new_max = 50.0
        self.UI.w_range.lf_min.setValue(new_min)
        self.UI.w_range.lf_max.setValue(new_max)

        dict_gen = self.UI.w_range.get_field_selected()

        assert dict_gen["min"] == new_min and dict_gen["max"] == new_max

        # Test 2 : Making sure that min and max are switched if min > max
        self.UI.w_range.lf_min.setValue(new_max)
        self.UI.w_range.lf_max.setValue(new_min)
        self.UI.w_range.update_needed()

        dict_gen = self.UI.w_range.get_field_selected()

        assert dict_gen["min"] == new_min and dict_gen["max"] == new_max

        # Test 3 : Checking that the unit is updated when changed
        if self.UI.w_range.c_unit.count() > 1:
            for index_unit in range(self.UI.w_range.c_unit.count()):
                self.UI.w_range.c_unit.setCurrentIndex(index_unit)

                dict_gen = self.UI.w_range.get_field_selected()

                assert dict_gen["unit"] == self.UI.w_range.c_unit.currentText()

    def check_string_dataselection(self):
        """Test to make sure that when DataSelection is modified, the string is updated correctly"""

        # Modifying the operation and making sure that the string is updated
        for wid in self.UI.w_axis_manager.w_data_sel:
            wid.blockSignals(True)
            for index_ope in range(wid.c_type_extraction.count()):

                wid.c_type_extraction.setCurrentIndex(index_ope)

                operation = wid.c_type_extraction.currentText()
                if operation == "slice":
                    assert (
                        wid.get_operation_selected()
                        == wid.axis.name
                        + type_extraction_dict[operation]
                        + str(wid.slider.value())
                        + "]"
                        + "{"
                        + wid.unit
                        + "}"
                    )
                elif operation in type_extraction_dict:
                    assert (
                        wid.get_operation_selected()
                        == wid.axis.name
                        + type_extraction_dict[operation]
                        + "{"
                        + wid.unit
                        + "}"
                    )
                else:
                    assert wid.get_operation_selected() == None

            wid.blockSignals(False)

        for wid in self.UI.w_axis_manager.w_data_sel:
            wid.blockSignals(True)
            for index_ope in range(wid.c_type_extraction.count()):

                wid.c_type_extraction.setCurrentIndex(index_ope)

                operation = wid.c_type_extraction.currentText()
                if operation == "slice":
                    # Modifying the slider (to put it at a different position)
                    index = 5
                    wid.slider.setValue(index)
                    action = parser.read_input_strings(
                        [wid.get_operation_selected()], axis_data=None
                    )
                    assert action[0].indices[0] == index

                    # Modifying the floatEdit by setting it to the initial value (index = 0)
                    wid.lf_value.setValue(wid.axis.initial)
                    wid.update_slider()
                    action = parser.read_input_strings(
                        [wid.get_operation_selected()], axis_data=None
                    )
                    assert action[0].indices[0] == 0


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()
    a.string_gen()
    a.teardown_class()
    print("Done")
