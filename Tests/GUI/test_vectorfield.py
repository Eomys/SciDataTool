import pytest
from PySide2.QtWidgets import *

from Tests.GUI import Field
from SciDataTool import DataLinspace, DataTime, Norm_ref, VectorField
import numpy as np


class TestGUI(object):
    @classmethod
    def setup_class(self):
        f = 50
        Time = DataLinspace(
            name="time",
            unit="s",
            initial=0,
            final=1 / f,
            number=10,
            include_endpoint=False,
        )

        Angle = DataLinspace(
            name="angle",
            unit="rad",
            initial=0,
            final=2 * np.pi,
            number=20,
            include_endpoint=False,
        )

        ta, at = np.meshgrid(Time.get_values(), Angle.get_values())
        field = 5 * np.cos(2 * np.pi * f * ta + 3 * at)

        Field_r = DataTime(
            name="Radial field",
            symbol="X_r",
            unit="m",
            normalizations={"ref": Norm_ref(ref=2e-5)},
            axes=[Time, Angle],
            values=field.T,
        )

        Field_t = DataTime(
            name="Tangential field",
            symbol="X_t",
            unit="m",
            normalizations={"ref": Norm_ref(ref=2e-5)},
            axes=[Time, Angle],
            values=-field.T,
        )

        self.VecField = VectorField(
            name="Example field",
            symbol="X",
            components={"radial": Field_r, "tangential": Field_t},
        )

        self.UI = self.VecField.plot(is_test=True)

    @pytest.mark.gui
    def check_component_selected(self):
        """Testing that when the user select a component, then it is used for the rest of the calculation"""

        for index_component in range(self.UI.w_vect_selector.c_component.count()):
            self.UI.w_vect_selector.c_component.setCurrentIndex(index_component)
            component_selected = self.UI.w_vect_selector.c_component.currentText()

            if component_selected in ["radial", "tangential", "axial"]:
                assert (
                    self.UI.data
                    == self.UI.data_obj.to_rphiz().components[component_selected]
                )

            elif component_selected in ["comp_x", "comp_y", "comp_z"]:
                assert (
                    self.UI.data
                    == self.UI.data_obj.to_xyz().components[component_selected]
                )

    @pytest.mark.gui
    def check_hide_show(self):
        """Testing that the UI is rightly updated as we are plotting a VectorField"""

        # Testing that the groupbox is shown
        assert not self.UI.w_vect_selector.isHidden()
        # Testing that the referential is hidden
        assert self.UI.w_vect_selector.c_referential.isHidden()
        assert self.UI.w_vect_selector.in_referential.isHidden()

        # Testing that axial and comp_z are not available if they are not in VectorField
        if not "axial" in self.VecField.components:
            components_list = list()
            for i in range(self.UI.w_vect_selector.c_component.count()):
                components_list.append(
                    self.UI.w_vect_selector.c_component.currentText()
                )

            assert not "axial" in components_list
            assert not "comp_z" in components_list

    @pytest.mark.gui
    def check_update_combobox(self):
        """Method to make sure that we update the combobox if coordinates are selected"""

        if not "axial" in self.VecField.components:
            # Case where we only have two axes for each set of coordinates
            self.UI.w_vect_selector.c_component.setCurrentIndex(0)
            assert self.UI.w_vect_selector.c_component.currentIndex() == 1

            self.UI.w_vect_selector.c_component.setCurrentIndex(3)
            assert self.UI.w_vect_selector.c_component.currentIndex() == 4

        else:
            # Case where we  have three axes for each set of coordinates
            self.UI.w_vect_selector.c_component.setCurrentIndex(0)
            assert self.UI.w_vect_selector.c_component.currentIndex() == 1

            self.UI.w_vect_selector.c_component.setCurrentIndex(4)
            assert self.UI.w_vect_selector.c_component.currentIndex() == 5


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing the checkbox
    a.check_hide_show()
    # Verifying the handling of the signals
    a.check_component_selected()
    # Checking that if the coordinates are selected in the combobox then we select the next item in the combobox
    a.check_update_combobox()

    print("Done")
