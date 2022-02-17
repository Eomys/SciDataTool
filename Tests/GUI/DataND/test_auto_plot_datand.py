from types import FrameType
import pytest

# from PySide2.QtWidgets import *
from PySide2 import QtWidgets
import sys

from numpy import pi
from numpy.random import random
from SciDataTool import DataLinspace, DataTime
from SciDataTool.Functions.Plot import ifft_dict
from SciDataTool.Functions import parser

a_p_list = list()

a_p_list.append(
    {
        "axis": ["time"],
        "action": ["angle[-1]", "z[2]"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot for XY plot

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z[2]"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot for 2D plot

a_p_list.append(
    {
        "axis": ["freqs"],
        "action": ["angle[-1]", "z[1]"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot for XY FFT plot

a_p_list.append(
    {
        "axis": ["freqs", "wavenumber"],
        "action": ["z[1]"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot for 2D FFT plot

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=sum"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot with sum as action on z

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=rms"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot with rms as action on z

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=rss"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot with rss as action on z


a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=mean"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot with mean as action on z

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [None],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot for 2D plot without giving any action


a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z[2]"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": None,
        "z_min": None,
        "z_max": None,
    }
)  # Testing the autoplot without WDataRange given

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [None],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": None,
        "z_min": None,
        "z_max": None,
    }
)  # Testing the autoplot for 2D plot without giving slice and WdataRange

a_p_list.append(
    {
        "axis": ["angle{°}", "time"],
        "action": ["z[2]"],
        "is_create_appli": False,
        "is_show_fig": False,
        "unit": "T",
        "z_min": 0,
        "z_max": 50,
    }
)  # Testing the autoplot for 2D plot where axes are inverted


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
    @pytest.mark.parametrize("test_dict", a_p_list)
    def test_check_a_p(self, test_dict):
        """Test to make sure that the auto-plot works as intended"""

        # Launching the auto plot with info from the dict
        if len(test_dict["axis"]) == 1:
            self.UI = self.Field.plot(
                test_dict["axis"][0],
                test_dict["action"][0],
                test_dict["action"][1],
                is_create_appli=test_dict["is_create_appli"],
                is_show_fig=test_dict["is_show_fig"],
                unit=test_dict["unit"],
                z_min=test_dict["z_min"],
                z_max=test_dict["z_max"],
            )

        elif len(test_dict["axis"]) == 2:
            self.UI = self.Field.plot(
                test_dict["axis"][0],
                test_dict["axis"][1],
                test_dict["action"][0],
                is_create_appli=test_dict["is_create_appli"],
                is_show_fig=test_dict["is_show_fig"],
                unit=test_dict["unit"],
                z_min=test_dict["z_min"],
                z_max=test_dict["z_max"],
            )

        # Recovering the string generated
        [_, axes_sent, actions_sent, drange] = self.UI.w_plot_manager.get_plot_info()

        axes_sent = parser.read_input_strings(axes_sent, axis_data=None)

        actions_sent = parser.read_input_strings(actions_sent, axis_data=None)

        # Step 1 : Checking the axes (1 and 2 if given)
        assert len(axes_sent) == len(test_dict["axis"])

        axes_given = parser.read_input_strings(test_dict["axis"], axis_data=None)

        # Checking the name of the axes
        assert axes_sent[0].name == axes_given[0].name

        # Checking the unit
        if axes_given[0].unit == "SI":
            # If the unit is not given, then we make sure that the unit by default is selected
            assert axes_sent[
                0
            ].unit == self.UI.w_plot_manager.w_axis_manager.w_axis_1.get_axis_unit_selected().split(
                "{"
            )[
                1
            ].rstrip(
                "}"
            )
        else:
            assert axes_sent[0].unit == axes_given[0].unit

        # Checking axis 2 if we have one
        if len(axes_sent) == 2:
            assert axes_sent[1].name == axes_given[1].name
            if axes_given[1].unit == "SI":
                # If the unit is not given, then we make sure that the unit by default is selected
                assert axes_sent[
                    1
                ].unit == self.UI.w_plot_manager.w_axis_manager.w_axis_2.get_axis_unit_selected().split(
                    "{"
                )[
                    1
                ].rstrip(
                    "}"
                )

        # Step 2 : Checking the actions
        if test_dict["action"] != [None]:

            actions_given = parser.read_input_strings(
                test_dict["action"], axis_data=None
            )
            assert len(actions_sent) == len(actions_given)

            for i in range(len(actions_sent)):
                # Checking the name of the axis
                assert actions_sent[i].name == actions_given[i].name

                # Checking the operation given
                assert actions_sent[i].extension == actions_given[i].extension

                # Special case when slice is the operation selected (we have to check the index)
                if actions_sent[i].extension == "single":

                    if actions_given[i].indices[0] < 0:
                        # if we gave a negative index, we have to update the value manually (slider accept/return only positive value)
                        assert (
                            self.UI.w_plot_manager.w_axis_manager.w_slice_op[
                                i
                            ].slider.value()
                            == self.UI.w_plot_manager.w_axis_manager.w_slice_op[
                                i
                            ].slider.maximum()
                            + actions_given[i].indices[0]
                        )
                    else:
                        assert (
                            self.UI.w_plot_manager.w_axis_manager.w_slice_op[
                                i
                            ].slider.value()
                            == actions_given[i].indices[0]
                        )

                # Checking the units
                if actions_given[i].unit == "SI":
                    assert (
                        # If the unit is not given, then we make sure that the unit by default is selected
                        actions_sent[i].unit
                        == self.UI.w_plot_manager.w_axis_manager.w_slice_op[i].unit
                    )
                else:
                    assert actions_sent[i].unit == actions_given[i].unit
        else:
            # If no action are specified, then we apply a slice on the first index for all the axes
            for i in range(len(actions_sent)):
                assert (
                    actions_sent[i].name
                    == self.UI.w_plot_manager.w_axis_manager.w_slice_op[i].axis.name
                )
                assert actions_sent[i].extension == "single"
                assert (
                    self.UI.w_plot_manager.w_axis_manager.w_slice_op[i].slider.value()
                    == 0
                )
                assert (
                    actions_sent[i].unit
                    == self.UI.w_plot_manager.w_axis_manager.w_slice_op[i].unit
                )

        # Comparing the info given to range with those emitted

        # Checking the unit of the field
        if test_dict["unit"] == None:
            assert drange["unit"] == self.UI.w_plot_manager.w_range.c_unit.currentText()
        else:
            assert drange["unit"] == test_dict["unit"]

        # To check the value of min and max when they are not given we have to do a get_along/get_magnitude_along to recover min and max
        if test_dict["z_min"] == None or test_dict["z_min"] == None:
            if len(axes_given) == 1:
                if axes_given[0].name in ifft_dict:
                    field_value = self.Field.get_magnitude_along(
                        self.UI.w_plot_manager.w_axis_manager.get_operation_selected()[
                            0
                        ],
                        self.UI.w_plot_manager.w_axis_manager.get_operation_selected()[
                            1
                        ],
                        self.UI.w_plot_manager.w_axis_manager.get_axes_selected()[0],
                    )
                else:
                    field_value = self.Field.get_along(
                        self.UI.w_plot_manager.w_axis_manager.get_operation_selected()[
                            0
                        ],
                        self.UI.w_plot_manager.w_axis_manager.get_operation_selected()[
                            1
                        ],
                        self.UI.w_plot_manager.w_axis_manager.get_axes_selected()[0],
                    )

            elif len(axes_given) == 2:
                if axes_given[0].name in ifft_dict and axes_given[1].name in ifft_dict:
                    field_value = self.Field.get_magnitude_along(
                        self.UI.w_plot_manager.w_axis_manager.get_operation_selected()[
                            0
                        ],
                        self.UI.w_plot_manager.w_axis_manager.get_axes_selected()[0],
                        self.UI.w_plot_manager.w_axis_manager.get_axes_selected()[1],
                    )
                else:
                    field_value = self.Field.get_along(
                        self.UI.w_plot_manager.w_axis_manager.get_operation_selected()[
                            0
                        ],
                        self.UI.w_plot_manager.w_axis_manager.get_axes_selected()[0],
                        self.UI.w_plot_manager.w_axis_manager.get_axes_selected()[1],
                    )
            if test_dict["z_min"] == None:
                # Making sure that the value are equal with a threshold of 1e-4
                eps = 1e-4
                assert drange["min"] - field_value[self.Field.symbol].min() < eps
            if test_dict["z_max"] == None:
                # Making sure that the value are equal with a threshold of 1e-4
                eps = 1e-4
                assert drange["max"] - field_value[self.Field.symbol].max() < eps
        else:
            # If min and max are given, we just have to compare them
            assert drange["min"] == float(test_dict["z_min"])
            assert drange["max"] == float(test_dict["z_max"])

        # Making sure that we update the name of g_data_extract with the plot selected
        title = self.UI.w_plot_manager.w_range.g_range.title()
        if len(test_dict["axis"]) == 1:
            assert title == "Y Range"
        elif len(test_dict["axis"]) == 2:
            assert title == "Z Range"


if __name__ == "__main__":

    for ii, a_p_test in enumerate(a_p_list):
        a = TestGUI()
        a.setup_class()
        a.test_check_a_p(a_p_test)
        print("Test n°" + str(ii) + " done")
