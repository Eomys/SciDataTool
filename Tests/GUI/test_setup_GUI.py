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
    def check_axes(self):
        """Checking that the axes_list inside WAxisSelector corresponds to the axes of Field"""
        axes_expected = [axis.name for axis in self.Field.get_axes()]
        assert self.UI.w_axis_manager.w_axis_1.axes_list == axes_expected
        # On the second axis, we also have None as a possibility
        axes_expected.insert(0, "None")
        assert self.UI.w_axis_manager.w_axis_2.axes_list == axes_expected

    @pytest.mark.gui
    def check_data_sel(self):
        """Checking the axis/axes of DataSelection have not been selected by the user before"""

        axes_selected = [
            self.UI.w_axis_manager.w_axis_1.get_current_axis_selected(),
            self.UI.w_axis_manager.w_axis_2.get_current_axis_selected(),
        ]

        for wid in self.UI.w_axis_manager.w_data_sel:
            assert not wid.axis in axes_selected

    @pytest.mark.gui
    def check_range(self):
        """Method that check that the units and the values of min and max set by default in the app corresponds to those of the field."""

        # Checking the unit of WDataRange
        assert self.Field.unit in self.UI.w_range.unit_list

        # Recovering the axis selected and their units
        axes_selected = self.UI.w_axis_manager.get_axes_selected()
        # Recovering the operation on the other axes
        data_selection = self.UI.w_axis_manager.get_operation_selected()

        axes_selected_parsed = parser.read_input_strings(axes_selected, axis_data=None)

        # Recovering the minimum and the maximum of the field
        if len(axes_selected) == 1:

            # Checking if the field is plotted in fft, then we use get_magnitude_along
            # Otherwise we use get_along

            if axes_selected_parsed[0].name in ifft_dict:
                field_value = self.Field.get_magnitude_along(
                    data_selection[0], data_selection[1], axes_selected[0]
                )
            else:
                field_value = self.Field.get_along(
                    data_selection[0], data_selection[1], axes_selected[0]
                )

            field_min = field_value[self.Field.symbol].min()
            field_max = field_value[self.Field.symbol].max()

        elif len(axes_selected) == 2:

            # Checking if the field is plotted in fft, then we use get_magnitude_along
            # Otherwise we use get_along
            if (
                axes_selected_parsed[0].name in ifft_dict
                and axes_selected_parsed[1].name in ifft_dict
            ):
                field_value = self.Field.get_magnitude_along(
                    data_selection[0], axes_selected[0], axes_selected[1]
                )
            else:
                field_value = self.Field.get_along(
                    data_selection[0], axes_selected[0], axes_selected[1]
                )

            field_min = field_value[self.Field.symbol].min()
            field_max = field_value[self.Field.symbol].max()

        # Checking that the values are close enough
        eps = 1e-5
        assert abs(field_min - self.UI.w_range.lf_min.value()) < eps
        assert abs(field_max - self.UI.w_range.lf_max.value()) < eps


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    a.check_axes()
    a.check_data_sel()
    a.check_range()

    a.teardown_class()
    print("Done")
