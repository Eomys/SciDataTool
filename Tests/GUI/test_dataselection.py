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
    def gen_dataselection(self):
        """Test that will make sure that the DataSelection is set up correctly according to the info given to him"""
        # Checking the interaction between the slider and floatEdit
        self.check_slider_floatEdit()
        # Checking the generation of the layout
        self.check_layout()

    def check_layout(self):
        """Test that the layout is set up according to the operation selected"""

        for wid in self.UI.w_axis_manager.w_data_sel:
            for ope in range(wid.c_type_extraction.count()):

                wid.blockSignals(True)
                wid.c_type_extraction.setCurrentIndex(ope)

                if wid.c_type_extraction.currentText() == "slice":
                    assert (
                        not wid.slider.isHidden()
                        and not wid.lf_value.isHidden()
                        and wid.b_action.isHidden()
                    )

                elif wid.c_type_extraction.currentText() == "slice (fft)":
                    assert (
                        not wid.slider.isHidden()
                        and not wid.lf_value.isHidden()
                        and wid.b_action.isHidden()
                    )

                elif wid.c_type_extraction.currentText() == "superimpose/filter":
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

    def check_slider_floatEdit(self):
        """Testing that the slider is updated correctly according to the slider and vice versa"""

        for wid in self.UI.w_axis_manager.w_data_sel:
            if wid.c_type_extraction.currentText() != "slice":
                wid.c_type_extraction.setCurrentIndex(0)

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
    a.gen_dataselection()
    a.teardown_class()
    print("Done")
