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
        self.init_table()

        if self.axis.name in axes_dict:
            self.setWindowTitle("Filtering on " + axes_dict[self.axis.name])
        else:
            self.setWindowTitle("Filtering on " + self.axis.name)

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

        if self.axis.is_components:
            # If we have an axis with components, then we use the filters to build the complete table
            filter_list = [filter for filter in self.axis.filter]
            filter_list.append("Plot ?")  # Adding the column with checkbox

            # Setting up the table
            self.tab_indices.setColumnCount(len(filter_list))
            self.tab_indices.setHorizontalHeaderLabels(filter_list)
            self.tab_indices.setRowCount(len(self.axis_values))

            for nrow in range(len(self.axis_values)):
                value = self.axis_values[nrow].split(self.axis.delimiter)

                for nvalue in range(len(value)):
                    # Adding value in right column
                    name_label = QLabel(str(value[nvalue]))
                    self.tab_indices.setCellWidget(
                        nrow,
                        nvalue,
                        name_label,
                    )

                # Adding Plot Checkbox
                is_plot = QCheckBox()
                self.tab_indices.setCellWidget(
                    nrow,
                    len(filter_list) - 1,
                    is_plot,
                )

        else:
            self.tab_indices.setColumnCount(2)
            self.tab_indices.setHorizontalHeaderLabels(["Value", "Plot ?"])
            self.tab_indices.setRowCount(len(self.axis_values))

            for nrow in range(len(self.axis_values)):
                value = self.axis_values[nrow]

                self.tab_indices.setRowCount(self.tab_indices.rowCount() + 1)

                # Adding index value
                name_label = QLabel(str(value))
                self.tab_indices.setCellWidget(
                    nrow,
                    0,
                    name_label,
                )

                # Adding Plot Checkbox
                is_plot = QCheckBox()
                self.tab_indices.setCellWidget(
                    nrow,
                    1,
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
