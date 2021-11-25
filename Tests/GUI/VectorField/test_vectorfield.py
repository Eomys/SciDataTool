import pytest
from PySide2 import QtWidgets
import sys
from Tests.GUI.VectorField import VecField


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

        cls.VecField = VecField
        cls.UI = cls.VecField.plot(is_show_fig=False, is_create_appli=False)

    @pytest.mark.gui
    def check_component_selected(self):
        """Testing that when the user select a component, then it is used for the rest of the calculation"""
        w_selector = self.UI.w_plot_manager.w_vect_selector

        for index_component in range(w_selector.c_component.count()):
            w_selector.c_component.setCurrentIndex(index_component)
            component_selected = w_selector.c_component.currentText()

            if component_selected in ["radial", "tangential", "axial"]:
                assert (
                    self.UI.w_plot_manager.data
                    == self.UI.w_plot_manager.data_obj.to_rphiz().components[
                        component_selected
                    ]
                )

            elif component_selected in ["comp_x", "comp_y", "comp_z"]:
                assert (
                    self.UI.w_plot_manager.data
                    == self.UI.w_plot_manager.data_obj.to_xyz().components[
                        component_selected
                    ]
                )

    @pytest.mark.gui
    def check_hide_show(self):
        """Testing that the UI is rightly updated as we are plotting a VectorField"""

        # Testing that the groupbox is shown
        assert not self.UI.w_plot_manager.w_vect_selector.isHidden()
        # Testing that the referential is hidden
        assert self.UI.w_plot_manager.w_vect_selector.c_referential.isHidden()
        assert self.UI.w_plot_manager.w_vect_selector.in_referential.isHidden()

        # Testing that axial and comp_z are not available if they are not in VectorField
        if not "axial" in self.VecField.components:
            components_list = list()
            for i in range(self.UI.w_plot_manager.w_vect_selector.c_component.count()):
                components_list.append(
                    self.UI.w_plot_manager.w_vect_selector.c_component.currentText()
                )

            assert not "axial" in components_list
            assert not "comp_z" in components_list

    @pytest.mark.gui
    def check_update_combobox(self):
        """Method to make sure that we update the combobox if coordinates are selected"""
        w_selector = self.UI.w_plot_manager.w_vect_selector

        if not "axial" in self.VecField.components:
            # Case where we only have two axes for each set of coordinates
            w_selector.c_component.setCurrentIndex(0)
            assert w_selector.c_component.currentIndex() == 1

            w_selector.c_component.setCurrentIndex(3)
            assert w_selector.c_component.currentIndex() == 4

        else:
            # Case where we  have three axes for each set of coordinates
            w_selector.c_component.setCurrentIndex(0)
            assert w_selector.c_component.currentIndex() == 1

            w_selector.c_component.setCurrentIndex(4)
            assert w_selector.c_component.currentIndex() == 5


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
