from ...GUI.DDataPlotter.DDataPlotter import DDataPlotter
from sys import argv, exit
from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
from SciDataTool.Functions import parser


def plot(self, *args, is_create_appli=True, is_test=False, **kwargs):
    """Plot the Data object in the GUI

    Parameters:
    -----------
    self : DataND
        A DataND object
    is_create_appli : bool
        True to create an QApplication
        (required if not already created)
    """

    if is_create_appli:
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        a = QApplication(argv)

    user_input_list = parser.read_input_strings(
        [arg for arg in args if arg != None], axis_data=None
    )
    user_input_dict = kwargs

    wid = DDataPlotter(self, user_input_list, user_input_dict)

    if is_test:
        return wid
    else:
        wid.show()

        if is_create_appli:
            exit(a.exec_())
