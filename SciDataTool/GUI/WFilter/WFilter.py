from PySide2.QtWidgets import QWidget, QCheckBox, QLabel
import matplotlib.pyplot as plt

from SciDataTool.GUI.WFilter.Ui_WFilter import Ui_WFilter
from PySide2.QtCore import Signal
from SciDataTool.Functions.Plot import axes_dict

# Column id
VALUE_COL = 0
PLOT_COL = 1


class WFilter(Ui_WFilter, QWidget):
    """Widget to select the Data/output range"""

    refreshNeeded = Signal()

    def __init__(self, axis, parent=None):
        """Linking the button with their method + initializing the arguments used

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        parent : QWidget
            The parent QWidget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.axis = axis
        self.axis_values = self.axis.get_values()

        if self.axis.name in axes_dict:
            self.setWindowTitle("Filtering on " + axes_dict[self.axis.name])
        else:
            self.setWindowTitle("Filtering on " + self.axis.name)

        self.init_table()

        self.b_Ok.clicked.connect(self.update_and_close)
        self.b_cancel.clicked.connect(self.cancel_and_close)

    def cancel_and_close(self):
        """Method called when the user click on the cancel button
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        self.close()

    def init_table(self):
        """Method that fill the table with the values of the axis, each line corresponds to one index
        Parameters
        ----------
        self : WDataRange
            a WDataRange object"""

        for i in range(len(self.axis_values)):
            self.add_row(i, self.axis_values[i])

    def add_row(self, nrow, value):
        """Add a new row to the table (filled with param)

        Parameters
        ----------
        self : DSensitivity
            A DSensitivity widget
        param : ParamExplorer
            ParamExplorer to display in the row
        """
        temp = self.tab_indices.rowCount() + 1
        self.tab_indices.setRowCount(temp)

        # Adding index value
        name_label = QLabel(str(value))
        self.tab_indices.setCellWidget(
            nrow,
            VALUE_COL,
            name_label,
        )

        # Adding Plot Checkbox
        is_plot = QCheckBox()
        self.tab_indices.setCellWidget(
            nrow,
            PLOT_COL,
            is_plot,
        )

    def update_and_close(self):
        """Method called when the click on the Ok button
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        self.close()
