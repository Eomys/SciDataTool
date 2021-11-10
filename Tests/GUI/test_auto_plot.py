from types import FrameType
import pytest
from PySide2.QtWidgets import *

from numpy import linspace, pi
from numpy.random import random
from SciDataTool import DataLinspace, DataTime
from SciDataTool.Functions.Plot import ifft_dict, fft_dict, unit_dict
from SciDataTool.Functions import NormError, parser

a_p_list = list()

a_p_list.append(
    {
        "axis": ["time"],
        "action": ["angle[-1]", "z[2]"],
        "is_create_appli": True,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot for XY plot

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z[2]"],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot for 2D plot

a_p_list.append(
    {
        "axis": ["freqs"],
        "action": ["angle[-1]", "z[1]"],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot for XY FFT plot

a_p_list.append(
    {
        "axis": ["freqs", "wavenumber"],
        "action": ["z[1]"],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot for 2D FFT plot

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=sum"],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot with sum as action on z

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=rms"],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot with rms as action on z

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=rss"],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot with rss as action on z


a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z=mean"],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot with mean as action on z

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [None],
        "is_create_appli": False,
        "is_test": True,
        "unit": "T",
        "zmin": "0",
        "zmax": "50",
    }
)  # Testing the autoplot for 2D plot without giving any action


a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": ["z[2]"],
        "is_create_appli": False,
        "is_test": True,
        "unit": None,
        "zmin": None,
        "zmax": None,
    }
)  # Testing the autoplot without WDataRange given

a_p_list.append(
    {
        "axis": ["time", "angle{°}"],
        "action": [None],
        "is_create_appli": False,
        "is_test": True,
        "unit": None,
        "zmin": None,
        "zmax": None,
    }
)  # Testing the autoplot for 2D plot without giving slice and WdataRange


class TestGUI(object):
    @classmethod
    def setup_class(self):
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

        self.Field = DataTime(
            name="Airgap flux density",
            symbol="B_r",
            unit="T",
            axes=[Time, Angle, Z],
            values=field,
        )

    @pytest.mark.gui
    @pytest.mark.parametrize("test_dict", a_p_list)
    def check_axis(self, test_dict):
        """Test to make sure that the auto-plot functions for its axes"""

        # Launching the auto plot according to the info given by the user
        if len(test_dict["axis"]) == 1:
            self.UI = self.Field.plot(
                test_dict["axis"][0],
                test_dict["action"][0],
                test_dict["action"][1],
                is_create_appli=test_dict["is_create_appli"],
                is_test=test_dict["is_test"],
                unit=test_dict["unit"],
                zmin=test_dict["zmin"],
                zmax=test_dict["zmax"],
            )

        elif len(test_dict["axis"]) == 2:
            self.UI = self.Field.plot(
                test_dict["axis"][0],
                test_dict["axis"][1],
                test_dict["action"][0],
                is_create_appli=test_dict["is_create_appli"],
                is_test=test_dict["is_test"],
                unit=test_dict["unit"],
                zmin=test_dict["zmin"],
                zmax=test_dict["zmax"],
            )

        # Recovering the string generated
        axes = self.UI.w_axis_manager.get_axes_selected()
        actions = self.UI.w_axis_manager.get_operation_selected()
        drange = self.UI.w_range.get_field_selected()

        print(axes)
        print(actions)
        print(drange)


if __name__ == "__main__":

    for ii, a_p_test in enumerate(a_p_list):
        a = TestGUI()
        a.setup_class()
        a.check_axis(a_p_test)
        print("Test n°" + str(ii) + " done")
