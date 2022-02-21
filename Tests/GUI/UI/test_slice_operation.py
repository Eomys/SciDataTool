import pytest
from PySide2 import QtWidgets
import sys
from Tests.GUI import Field


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
    def test_check_layout(self):
        """Test that the layout is set up according to the operation selected"""

        for wid in self.UI.w_plot_manager.w_axis_manager.w_slice_op:
            for ope in range(wid.c_operation.count()):

                wid.blockSignals(True)
                wid.c_operation.setCurrentIndex(ope)

                if wid.c_operation.currentText() == "slice":
                    assert (
                        not wid.slider.isHidden()
                        and not wid.lf_value.isHidden()
                        and wid.b_action.isHidden()
                    )

                elif wid.c_operation.currentText() == "slice (fft)":
                    assert (
                        not wid.slider.isHidden()
                        and not wid.lf_value.isHidden()
                        and wid.b_action.isHidden()
                    )

                elif wid.c_operation.currentText() == "overlay":
                    assert (
                        wid.slider.isHidden()
                        and wid.lf_value.isHidden()
                        and not wid.b_action.isHidden()
                    )

                else:
                    assert (
                        wid.slider.isHidden()
                        and wid.lf_value.isHidden()
                        and wid.b_action.isHidden()
                    )

                wid.blockSignals(False)

    @pytest.mark.gui
    def test_check_slider_floatEdit(self):
        """Testing that the slider is updated correctly according to the slider and vice versa"""

        for wid in self.UI.w_plot_manager.w_axis_manager.w_slice_op:
            if not wid.c_operation.currentText() in ["slice", "slice (fft)"]:
                wid.c_operation.setCurrentIndex(0)

            # Making sure that we have the same number of index inside the slider as in axis_value
            assert (wid.slider.maximum() - wid.slider.minimum() + 1) == len(
                wid.axis_value
            )
            # Modifying the value of the slider and checking if the floatEdit change correctly
            wid.slider.setValue(0)
            assert wid.lf_value.value() == wid.axis_value[wid.slider.value()]

            # Modifying the floatEdit and making sure that the slider is at the right index
            wid.lf_value.setValue(wid.axis_value[-1])
            wid.update_slider()
            assert wid.axis_value[wid.slider.value()] == wid.axis_value[-1]


if __name__ == "__main__":
    a = TestGUI()
    a.setup_class()

    # Checking the interaction between the slider and floatEdit
    a.test_check_slider_floatEdit()
    # Checking the generation of the layout
    a.test_check_layout()

    print("Done")
