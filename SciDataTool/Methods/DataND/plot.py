from ...GUI.DDataPlotter.DDataPlotter import DDataPlotter
from sys import argv, exit
from PySide2.QtWidgets import QApplication


def plot(self, is_create_appli=True):
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

    wid = DDataPlotter(data=self)
    wid.show()

    if is_create_appli:
        exit(a.exec_())