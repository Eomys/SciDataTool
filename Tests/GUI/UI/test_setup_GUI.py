import pytest
from PySide2 import QtWidgets
import sys
from Tests.GUI import Field
from SciDataTool.Functions.Plot import ifft_dict
from SciDataTool.Functions import parser


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
    def test_check_axes(self):
        """Checking that the axes_list inside WAxisSelector corresponds to the axes of Field"""
        axes_expected = [axis.name for axis in Field.get_axes()]
        assert self.UI.w_plot_manager.w_axis_manager.w_axis_1.axes_list == axes_expected
        # On the second axis, we also have None as a possibility
        axes_expected.insert(0, "None")
        assert self.UI.w_plot_manager.w_axis_manager.w_axis_2.axes_list == axes_expected

    @pytest.mark.gui
    def test_check_data_sel(self):
        """Checking the axis/axes of DataSelection have not been selected by the user before"""

        axes_selected = [
            self.UI.w_plot_manager.w_axis_manager.w_axis_1.get_axis_selected(),
            self.UI.w_plot_manager.w_axis_manager.w_axis_2.get_axis_selected(),
        ]

        for wid in self.UI.w_plot_manager.w_axis_manager.w_slice_op:
            assert not wid.axis in axes_selected

    @pytest.mark.gui
    def test_check_range(self):
        """Method that check that the units and the values of min and max set by default in the app corresponds to those of the field."""

        # Checking the unit of WDataRange
        assert Field.unit == self.UI.w_plot_manager.w_range.c_unit.currentText()

        # Recovering the axis selected and their units
        axes_selected = self.UI.w_plot_manager.w_axis_manager.get_axes_selected()
        # Recovering the operation on the other axes
        data_selection = self.UI.w_plot_manager.w_axis_manager.get_operation_selected()

        axes_selected_parsed = parser.read_input_strings(axes_selected, axis_data=None)

        # Recovering the minimum and the maximum of the field
        if len(axes_selected) == 1:
            # Checking that the right name is given to the groupBow with WDataRange
            assert self.UI.w_plot_manager.w_range.g_range.title() == "Y Range"

            # Checking if the field is plotted in fft, then we use get_magnitude_along
            # Otherwise we use get_along

            if axes_selected_parsed[0].name in ifft_dict:
                field_value = Field.get_magnitude_along(
                    data_selection[0], data_selection[1], axes_selected[0]
                )
            else:
                field_value = Field.get_along(
                    data_selection[0], data_selection[1], axes_selected[0]
                )

            field_min = field_value[Field.symbol].min()
            field_max = field_value[Field.symbol].max()

        elif len(axes_selected) == 2:
            # Checking that the right name is given to the groupBow with WDataRange
            assert self.UI.w_plot_manager.w_range.g_range.title() == "Z"

            # Checking if the field is plotted in fft, then we use get_magnitude_along
            # Otherwise we use get_along
            if (
                axes_selected_parsed[0].name in ifft_dict
                and axes_selected_parsed[1].name in ifft_dict
            ):
                field_value = Field.get_magnitude_along(
                    data_selection[0], axes_selected[0], axes_selected[1]
                )
            else:
                field_value = Field.get_along(
                    data_selection[0], axes_selected[0], axes_selected[1]
                )

            field_min = field_value[Field.symbol].min()
            field_max = field_value[Field.symbol].max()

        # Taking into account the delta that we add to improve the plot
        delta = field_max - field_min

        # Checking that the values are close enough
        eps = 1e-4
        assert (
            abs(
                field_min - delta * 0.05 - self.UI.w_plot_manager.w_range.lf_min.value()
            )
            < eps
        )
        assert (
            abs(
                field_max + delta * 0.05 - self.UI.w_plot_manager.w_range.lf_max.value()
            )
            < eps
        )


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    a.test_check_axes()
    a.test_check_data_sel()
    a.test_check_range()

    print("Done")
