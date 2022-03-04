import pytest
import sys
from PySide2 import QtWidgets

from Tests.GUI.VectorField import VecField
from numpy.testing import assert_almost_equal
from SciDataTool.Functions import parser

a_p_list = list()

a_p_list.append(
    {
        "axis": ["time"],
        "action": ["angle[-1]"],
        "is_create_appli": False,
        "is_show_fig": False,
        "component": "comp_x",
    }
)  # Testing the autoplot for XY plot and component 'comp_x'

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [],
        "is_create_appli": False,
        "is_show_fig": False,
        "component": "comp_x",
    }
)  # Testing the autoplot for 2D plot and component 'comp_x'

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [],
        "is_create_appli": False,
        "is_show_fig": False,
        "component": "comp_y",
    }
)  # Testing the autoplot for 2D plot and component 'comp_y'

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [],
        "is_create_appli": False,
        "is_show_fig": False,
        "component": "radial",
    }
)  # Testing the autoplot for 2D plot and component 'radial'

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [],
        "is_create_appli": False,
        "is_show_fig": False,
        "component": "tangential",
    }
)  # Testing the autoplot for 2D plot and component 'tangential'

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [],
        "is_create_appli": False,
        "is_show_fig": False,
        "component": "axial",
    }
)  # Testing the autoplot with an unavaible component


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

        cls.VecField = VecField

    @pytest.mark.gui
    @pytest.mark.parametrize("test_dict", a_p_list)
    def test_check_a_p(self, test_dict):
        """Test to make sure that the auto-plot works as intended"""

        # Launching the auto plot with info from the dict
        if len(test_dict["axis"]) == 1:
            self.UI = self.VecField.plot(
                test_dict["axis"][0],
                test_dict["action"][0],
                is_create_appli=test_dict["is_create_appli"],
                is_show_fig=test_dict["is_show_fig"],
                component=test_dict["component"],
            )

        elif len(test_dict["axis"]) == 2:
            self.UI = self.VecField.plot(
                test_dict["axis"][0],
                test_dict["axis"][1],
                is_create_appli=test_dict["is_create_appli"],
                is_show_fig=test_dict["is_show_fig"],
                component=test_dict["component"],
            )

        # Step 0 : Making sure that the components in the combobox :
        if (
            "axial" not in self.VecField.components
            or "comp_z" not in self.VecField.components
        ):
            assert self.UI.w_plot_manager.w_vect_selector.component_list == [
                "radial",
                "circumferential",
                "x-axis component",
                "y-axis component",
            ]
        else:
            assert self.UI.w_plot_manager.w_vect_selector.component_list == [
                "radial",
                "circumferential",
                "axial",
                "x-axis component",
                "y-axis component",
                "z-axis component",
            ]

        # Step 1 :  making sure that the right component is selected
        if test_dict["component"] in ["radial"]:
            assert_almost_equal(
                self.UI.w_plot_manager.data.values,
                VecField.to_rphiz().components[test_dict["component"]].values,
                7,
            )

        elif test_dict["component"] in ["comp_x", "comp_y"]:
            assert_almost_equal(
                self.UI.w_plot_manager.data.values,
                VecField.to_xyz().components[test_dict["component"]].values,
                7,
            )

        elif (
            test_dict["component"] == "axial"
            and test_dict["component"] in self.VecField.components
        ):
            assert_almost_equal(
                self.UI.w_plot_manager.data.values,
                VecField.to_xyz().components[test_dict["component"]].values,
                7,
            )

        elif (
            test_dict["component"] == "comp_z"
            and test_dict["component"] in self.VecField.components
        ):
            assert_almost_equal(
                self.UI.w_plot_manager.data.values,
                VecField.to_xyz().components[test_dict["component"]].values,
                7,
            )

        elif (
            test_dict["component"] == "tangential"
            and test_dict["component"] in self.VecField.components
        ):
            assert_almost_equal(
                self.UI.w_plot_manager.data.values,
                VecField.to_rphiz().components[test_dict["component"]].values,
                7,
            )

        else:
            assert_almost_equal(
                self.UI.w_plot_manager.data.values,
                VecField.to_rphiz().components["radial"].values,
                7,
            )

        # Step 2 : Checking that the axes and the operations given/sent are correct
        # Recovering the string generated
        axes_sent = parser.read_input_strings(
            self.UI.w_plot_manager.w_axis_manager.get_axes_selected(), axis_data=None
        )

        actions_sent = parser.read_input_strings(
            self.UI.w_plot_manager.w_axis_manager.get_operation_selected(),
            axis_data=None,
        )

        # Step 2-1 : Checking the axes (1 and 2 if given)
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
                assert (
                    axes_sent[1].unit
                    == self.UI.w_plot_manager.w_axis_manager.w_axis_2.get_current_unit()
                )

        # Step 2-2 : Checking the actions
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
                        # if we gave a negative index, we have to update the value nmanally (slider accept/return only positive value)
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
                assert actions_sent[i].indices[0] == 0
                assert (
                    actions_sent[i].unit
                    == self.UI.w_plot_manager.w_axis_manager.w_slice_op[i].unit
                )


if __name__ == "__main__":

    for ii, a_p_test in enumerate(a_p_list):
        a = TestGUI()
        a.setup_class()
        a.test_check_a_p(a_p_test)
        print("Test n°" + str(ii) + " done")
