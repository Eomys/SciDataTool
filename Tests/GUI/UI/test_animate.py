from os.path import isfile
from os import remove
import pytest
from PySide2 import QtWidgets
import sys
from SciDataTool import DataPattern, DataLinspace, DataTime
from tenacity import sleep
from Tests.GUI import Field
from numpy.random import random
from numpy import pi


class TestGUI(object):
    @classmethod
    def setup_class(cls):
        """Run at the begining of every test to setup the gui"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

        # Slice = DataPattern(
        #     name="z",
        #     unit="m",
        #     values=[-1, -0.5],
        #     is_step=True,
        #     values_whole=[-1, -0.5, 0.5, 1],
        #     rebuild_indices=[0, 1, 1, 0],
        #     unique_indices=[0, 1, 1, 0],
        # )

        # f = 50
        # Nt_tot = 16
        # Na_tot = 20

        # Time = DataLinspace(
        #     name="time", unit="s", initial=0, final=1 / (2 * f), number=Nt_tot
        # )
        # Angle = DataLinspace(
        #     name="angle", unit="rad", initial=0, final=2 * pi, number=Na_tot
        # )
        # Z = DataLinspace(name="z", unit="m", initial=-1, final=1, number=3)

        # field = random((Nt_tot, Na_tot, 2))

        # Field = DataTime(
        #     name="Airgap flux density",
        #     symbol="B_r",
        #     unit="T",
        #     axes=[Time, Angle, Slice],
        #     values=field,
        # )

        cls.Field = Field
        cls.UI = cls.Field.plot(is_show_fig=False, is_create_appli=False)

    @classmethod
    def teardown_class(cls):
        """Exit the app after the test"""
        cls.app.quit()

    @pytest.mark.gui
    def test_check_animation_2D(self):
        """Testing that when the user click on the animate button, then animation is created and stored at the right place"""

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_angle = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0]
        assert w_slice_angle.axis_name == "angle"
        w_slice_angle.is_animate = True
        w_slice_angle.generateAnimation.emit()
        sleep(30)

        path_to_gif = self.UI.w_plot_manager.gif_path_list.pop(-1)

        # Making sure that the gif is saved at the right place
        assert isfile(path_to_gif) == True

        # Closing the animation
        self.UI.w_plot_manager.close_all_gif()

        # Deleting gif for future test
        remove(path_to_gif)

    @pytest.mark.gui
    def test_close_few_animation(self):
        """Testing that the animation are correctly closed when there are more than one displayed"""

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_angle = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0]
        assert w_slice_angle.axis_name == "angle"
        w_slice_angle.is_animate = True
        w_slice_angle.generateAnimation.emit()
        sleep(30)

        path_to_file_a = self.UI.w_plot_manager.gif_path_list[-1]

        # Making sure that the gif are saved at the right place
        assert isfile(path_to_file_a) == True

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_z = self.UI.w_plot_manager.w_axis_manager.w_slice_op[1]
        assert w_slice_z.axis_name == "z"
        w_slice_z.is_animate = True
        w_slice_z.generateAnimation.emit()
        sleep(30)

        path_to_file_z = self.UI.w_plot_manager.gif_path_list[-1]

        # Making sure that the gif are saved at the right place
        assert isfile(path_to_file_z) == True

        # Closing the animation
        self.UI.w_plot_manager.close_all_gif()

        # Deleting gif for future test
        remove(path_to_file_a)
        remove(path_to_file_z)

    @pytest.mark.gui
    def test_check_animation_3D(self):
        """Testing that when the user click on the animate button, then animation is created and stored at the right place"""

        # Selecting an axis on Y to go 3D
        self.UI.w_plot_manager.w_axis_manager.w_axis_2.c_axis.setCurrentIndex(1)

        # Selection WSliceOperator + emitting signal to generate animation
        w_slice_angle = self.UI.w_plot_manager.w_axis_manager.w_slice_op[0]
        assert w_slice_angle.axis_name == "z"
        w_slice_angle.is_animate = True
        w_slice_angle.generateAnimation.emit()
        sleep(60)

        path_to_file = self.UI.w_plot_manager.gif_path_list.pop(-1)

        # Making sure that the gif is saved at the right place
        assert isfile(path_to_file) == True

        # Closing the animation
        self.UI.w_plot_manager.close_all_gif()

        # Deleting gif for future test
        remove(path_to_file)


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # # Testing that the gif is created and located at the right path (2D plot)
    # a.test_check_animation_2D()

    # # Testing that the animations are closed correctly
    # a.test_close_few_animation()

    # # Testing that the gif is created and located at the right path (3D plot)
    # a.test_check_animation_3D()

    # a.teardown_class()
    print("Done")
