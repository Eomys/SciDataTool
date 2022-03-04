from SciDataTool.GUI.DDataPlotter.DDataPlotter import DDataPlotter
from sys import argv, exit
from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
from SciDataTool.Functions import parser

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


def plot(
    self,
    *args,
    component=None,
    unit=None,
    z_min=None,
    z_max=None,
    is_auto_refresh=False,
    is_show_fig=True,
    is_create_appli=True,
    frozen_type=0,
):
    """Plot the Data object in the GUI

    Parameters:
    -----------
    self : VectorField
        A VectorField object
    *args : 1 or 2 str
        Example ("time", "angle[0]") or ("angle")
    component : str
        Name of the component to plot (For VectorField only)
    unit : str
        unit in which to plot the field
    z_min : float
        Minimum value for Z axis (or Y if only one axe)
    z_max : float
        Minimum value for Z axis (or Y if only one axe)
    is_auto_refresh : bool
        True to refresh at each widget changed (else wait call to button)
    is_show_fig : bool
        To show the GUI or return the widget (False for testing)
    is_create_appli : bool
        True to create an QApplication (required if not already created by another GUI)
    frozen_type : int
        0 to let the user modify the axis of the plot, 1 to let him switch them, 2 to not let him change them, 3 to freeze both axes and operations, 4 to freeze fft
    """

    if is_create_appli:
        a = QApplication(argv)

    # Parse the first arguments to get the axes
    axes_request_list = parser.read_input_strings(
        [arg for arg in args if arg != None], axis_data=None
    )

    if unit is None:
        unit = self.components[list(self.components.keys())[0]].unit

    wid = DDataPlotter(
        data=self,
        axes_request_list=axes_request_list,
        component=component,
        unit=unit,
        z_min=z_min,
        z_max=z_max,
        is_auto_refresh=is_auto_refresh,
        frozen_type=frozen_type,
    )

    if is_show_fig:
        wid.show()

    if is_create_appli:
        exit(a.exec_())
    else:
        return wid
