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

        path_to_gif = self.UI.w_plot_manager.gif_path_list[0]

        # Making sure that the gif is saved at the right place
        assert isfile(path_to_gif) == True

        # Closing the animation
        self.UI.close()

        # Deleting gif for future test
        remove(path_to_gif)

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

        path_to_file = self.UI.w_plot_manager.gif_path_list[0]

        # Making sure that the gif is saved at the right place
        assert isfile(path_to_file) == True

        # Closing the animation
        self.UI.close()

        # Deleting gif for future test
        remove(path_to_file)

    @pytest.mark.gui
    def test_close_few_animation(self):
        """Testing that the animation are correctly closed when there are more than one displayed"""

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_angle = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0]
        assert w_slice_angle.axis_name == "angle"
        w_slice_angle.b_animate.clicked.emit()
        sleep(30)

        path_to_file_a = self.UI.w_plot_manager.gif_path_list[0]

        # Making sure that the gif are saved at the right place
        assert isfile(path_to_file_a) == True

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_z = self.UI.w_plot_manager.w_axis_manager.w_slice_op[1]
        assert w_slice_z.axis_name == "z"
        w_slice_z.b_animate.clicked.emit()
        sleep(30)

        path_to_file_z = self.UI.w_plot_manager.gif_path_list[1]

        # Making sure that the gif are saved at the right place
        assert isfile(path_to_file_z) == True

        # Closing the animation
        self.UI.close()

        # Deleting gif for future test
        remove(path_to_file_a)
        remove(path_to_file_z)


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Testing that the gif is created and located at the right path (2D plot)
    a.test_check_ankimation_2D()

    # Testing that the gif is created and located at the right path (3D plot)
    # a.test_check_animation_3D()

    # Testing that the animations are closed correctly
    # a.test_close_few_animation()

    print("Done")
