from os.path import isfile
from os import remove
import pytest
from PySide2 import QtWidgets
import sys

from tenacity import sleep
from Tests.GUI import Field


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

        cls.Field = Field
        cls.UI = cls.Field.plot(is_show_fig=False, is_create_appli=False)

    @pytest.mark.gui
    def test_check_animation_2D(self):
        """Testing that when the user click on the animate button, then animation is created and stored at the right place"""

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_angle = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0]
        assert w_slice_angle.axis_name == "angle"
        w_slice_angle.b_animate.clicked.emit()
        sleep(30)

        # Making sure that the gif is saved at the right place
        assert isfile(self.UI.w_plot_manager.gif) == True

        # Closing the animation
        self.UI.close()

        # Deleting gif for future test
        remove(self.UI.w_plot_manager.gif)

    @pytest.mark.gui
    def test_check_animation_3D(self):
        """Testing that when the user click on the animate button, then animation is created and stored at the right place"""

        # Selecting an axis on Y to go 3D
        self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(1)

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_angle = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0]
        assert w_slice_angle.axis_name == "z"
        w_slice_angle.b_animate.clicked.emit()
        sleep(60)

        # Making sure that the gif is saved at the right place
        assert isfile(self.UI.w_plot_manager.gif) == True

        # Closing the animation
        self.UI.close()

        # Deleting gif for future test
        remove(self.UI.w_plot_manager.gif)


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing that the gif is created and located at the right path
    a.test_check_animation_2D()

    # Testing that the gif is created and located at the right path
    # a.test_check_animation_3D()

    print("Done")
