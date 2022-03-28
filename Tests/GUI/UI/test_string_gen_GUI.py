import pytest
from PySide2 import QtWidgets
import sys
from Tests.GUI import Field
from SciDataTool.Functions.Plot import ifft_dict, fft_dict, axes_dict
from SciDataTool.Functions import parser
from SciDataTool.GUI.WSliceOperator.WSliceOperator import type_extraction_dict


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
    def test_check_axes_strings(self):
        "Testing that the string generated corresponds to the info given by the user"
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1
        axis_2 = self.UI.w_plot_manager.w_axis_manager.w_axis_2

        for index_axis_1 in range(axis_1.c_axis.count()):
            axis_1.c_axis.setCurrentIndex(index_axis_1)
            for index_axis_2 in range(axis_2.c_axis.count()):
                axis_2.c_axis.setCurrentIndex(index_axis_2)

                axes_selected = parser.read_input_strings(
                    self.UI.w_plot_manager.w_axis_manager.get_axes_selected(),
                    axis_data=None,
                )

                # Checking that the axis string is correct
                if axes_selected[0].name in ifft_dict:
                    assert (
                        ifft_dict[axes_selected[0].name] == axis_1.c_axis.currentText()
                        and axis_1.c_action.currentText() == "FFT"
                    )

                elif axes_selected[0].name in axes_dict:
                    assert (
                        axes_dict[axes_selected[0].name] == axis_1.c_axis.currentText()
                    )

                else:
                    assert axes_selected[0].name == axis_1.c_axis.currentText()
                # Checking that the unit in the string is correct
                assert axes_selected[0].unit == axis_1.c_unit.currentText()

                # if an axis is selected on axis 2 the we check its string as well
                if len(axes_selected) == 2:

                    # Checking that the axis string is correct
                    if axes_selected[1].name in ifft_dict:
                        assert (
                            ifft_dict[axes_selected[1].name]
                            == axis_2.c_axis.currentText()
                            and axis_2.c_action.currentText() == "FFT"
                        )

                    elif axes_selected[1].name in axes_dict:
                        assert (
                            axes_dict[axes_selected[1].name]
                            == axis_2.c_axis.currentText()
                        )

                    else:
                        assert axes_selected[1].name == axis_2.c_axis.currentText()
                    # Checking that the unit in the string is correct
                    assert axes_selected[1].unit == axis_2.c_unit.currentText()

    @pytest.mark.gui
    def test_check_axis_updated(self):
        """Test to make sure that when we switch from time to frequency (or from angle to wavenb), the string is updated correclty"""
        axis_1 = self.UI.w_plot_manager.w_axis_manager.w_axis_1
        axis_2 = self.UI.w_plot_manager.w_axis_manager.w_axis_2

        for index_axis in range(axis_1.c_axis.count()):
            axis_1.c_axis.setCurrentIndex(index_axis)
            axes = list()

            if axis_1.get_axis_selected() in fft_dict:
                # Recovering the string when '' is selected
                axis_1.c_action.setCurrentIndex(0)
                axes.append(axis_1.get_axis_unit_selected())
                # Recovering the string when 'FFT' is selected
                axis_1.c_action.setCurrentIndex(1)
                axes.append(axis_1.get_axis_unit_selected())
                # Processing the string to compare them
                axes_parsed = parser.read_input_strings(axes, axis_data=None)

                assert axes_parsed[1].name == fft_dict[axes_parsed[0].name]

    @pytest.mark.gui
    def test_check_range_updated(self):
        """Testing how WDataRange string are generated after updating the widget"""

        # Test 1 : Making sure that min and max are updated
        new_min = 15.0
        new_max = 50.0
        self.UI.w_plot_manager.w_range.lf_min.setValue(new_min)
        self.UI.w_plot_manager.w_range.lf_max.setValue(new_max)

        dict_gen = self.UI.w_plot_manager.w_range.get_field_selected()

        assert dict_gen["min"] == new_min and dict_gen["max"] == new_max

        # Test 2 : Making sure that min and max are switched if min > max
        self.UI.w_plot_manager.w_range.lf_min.setValue(new_max)
        self.UI.w_plot_manager.w_range.lf_max.setValue(new_min)
        self.UI.w_plot_manager.w_range.update_needed()

        dict_gen = self.UI.w_plot_manager.w_range.get_field_selected()

        assert dict_gen["min"] == new_min and dict_gen["max"] == new_max

        # Test 3 : Checking that the unit is updated when changed
        if self.UI.w_plot_manager.w_range.c_unit.count() > 1:
            for index_unit in range(self.UI.w_plot_manager.w_range.c_unit.count()):
                self.UI.w_plot_manager.w_range.c_unit.setCurrentIndex(index_unit)

                dict_gen = self.UI.w_plot_manager.w_range.get_field_selected()

                assert (
                    dict_gen["unit"]
                    == self.UI.w_plot_manager.w_range.c_unit.currentText()
                )

    @pytest.mark.gui
    def test_check_string_dataselection(self):
        """Test to make sure that when DataSelection is modified, the string is updated correctly"""

        # Modifying the operation and making sure that the string is updated
        for wid in self.UI.w_plot_manager.w_axis_manager.w_slice_op:
            wid.blockSignals(True)
            for index_ope in range(wid.c_operation.count()):

                wid.c_operation.setCurrentIndex(index_ope)

                operation = wid.c_operation.currentText()
                if operation == "slice":
                    assert wid.get_operation_selected() == (
                        wid.axis.name
                        + "="
                        + str(wid.lf_value.value())
                        + "{"
                        + wid.unit
                        + "}",
                        False,
                    )
                elif operation == "slice (fft)":
                    assert wid.get_operation_selected() == (
                        fft_dict[wid.axis.name] + "=" + str(wid.lf_value.value()),
                        None,
                    )
                elif operation.split(" ")[0] in type_extraction_dict:
                    assert wid.get_operation_selected() == (
                        wid.axis.name
                        + type_extraction_dict[operation.split(" ")[0]]
                        + "{"
                        + wid.unit
                        + "}",
                        None,
                    )
                else:
                    assert wid.get_operation_selected() == None

            wid.blockSignals(False)

        for wid in self.UI.w_plot_manager.w_axis_manager.w_slice_op:
            wid.blockSignals(True)
            for index_ope in range(wid.c_operation.count()):

                wid.c_operation.setCurrentIndex(index_ope)

                operation = wid.c_operation.currentText()
                if operation == "slice":
                    # Modifying the slider (to put it at a different position)
                    index = 5
                    wid.slider.setValue(index)
                    action = parser.read_input_strings(
                        [wid.get_operation_selected()[0]], axis_data=None
                    )
                    assert action[0].input_data[0] == wid.lf_value.value()

                    # Modifying the floatEdit by setting it to the initial value (index = 0)
                    wid.lf_value.setValue(wid.axis.initial)
                    wid.update_slider()
                    action = parser.read_input_strings(
                        [wid.get_operation_selected()[0]], axis_data=None
                    )
                    assert action[0].input_data[0] == wid.lf_value.value()


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Checking that the string generated for the axes are correct
    a.test_check_axes_strings()
    # Making sure that the string is updated according to the change of the UI (FFT to '' for ex)
    a.test_check_axis_updated()
    # When modifying WDataRange, making sure that the string is updated correctly
    a.test_check_range_updated()
    # When modifying DataSelection, making sure that the string is updated correctly (slice to sum for ex)
    a.test_check_string_dataselection()

    print("Done")
