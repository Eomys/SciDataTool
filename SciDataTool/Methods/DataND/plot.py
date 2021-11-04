from ...GUI.DDataPlotter.DDataPlotter import DDataPlotter
from sys import argv, exit
from PySide2.QtWidgets import QApplication
from SciDataTool.Functions import parser


def plot(self, *args, is_create_appli=True, **kwargs):
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
        a = QApplication(argv)

    user_input_list = parser.read_input_strings(args, axis_data=None)
    user_input_dict = kwargs

    wid = DDataPlotter(self, user_input_list, user_input_dict)
    wid.show()

    if is_create_appli:
        exit(a.exec_())
