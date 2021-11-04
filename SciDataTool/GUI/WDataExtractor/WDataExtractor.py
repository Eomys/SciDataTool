from PySide2.QtWidgets import QWidget

from ...GUI.WDataExtractor.Ui_WDataExtractor import Ui_WDataExtractor
from PySide2.QtCore import Signal
from ...Functions.Plot import axes_dict
from ...Classes.Data import Data
from numpy import where
from numpy import argmin, abs as np_abs

type_extraction_dict = {
    "slice": "[",
    "rms": "=rms",
    "rss": "=rss",
    "sum": "=sum",
    "mean": "=mean",
}


class WDataExtractor(Ui_WDataExtractor, QWidget):
    """Widget to define how to handle the 'non-plot' axis"""

    refreshNeeded = Signal()

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        parent : QWidget
            The parent QWidget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.name = "angle"
        self.axis = Data

        self.c_type_extraction.currentTextChanged.connect(self.update_layout)
        self.slider.valueChanged.connect(self.update_floatEdit)
        self.lf_value.editingFinished.connect(self.update_slider)

    def get_actionSelected(self):
        """Method that return a string of the action selected by the user on the axis of the widget.
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object

        Output
        ---------
        string
            name of the current action selected
        """

        # Recovering the action selected by the user
        action_type = self.c_type_extraction.currentText()

        if action_type == "slice":
            slice_index = self.slider.value()
            action = type_extraction_dict[action_type] + str(slice_index) + "]"

        else:
            action = type_extraction_dict[action_type]

        return self.axis.name + action + "{" + self.unit + "}"

    def get_name(self):
        """Method that return the name of the axis of the WDataExtractor
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        """
        return self.name

    def set_name(self, name):
        """Method that set the name of the axis of the WDataExtractor
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        name : string
            string that hold the name of the axis
        """
        if name in axes_dict:
            self.in_name.setText(axes_dict[name])
        else:
            self.in_name.setText(name)

        self.name = name

    def set_op(self, user_input):

        # Recovering the type of the operation and on which axis we are applying it
        op_type = user_input.extension
        op_name = user_input.name

        # Setting the label with the right name
        self.set_name(op_name)

        # Converting type of the operation if we have a slice or a superimpose/filter
        if op_type == "single":
            op_type = "slice"

        elif op_type == "list":
            op_type = "superimpose/filter"

        # Setting operation combobox
        self.c_type_extraction.blockSignals(True)

        for i in range(self.c_type_extraction.count()):
            self.c_type_extraction.setCurrentIndex(i)

            if self.c_type_extraction.currentText() == op_type:
                break

        self.c_type_extraction.blockSignals(False)
        self.update_layout()

        # setting slider

        if op_type == "slice":
            self.set_slider(user_input.indices[0])

    def set_slider(self, index):

        self.slider.blockSignals(True)
        self.slider.setValue(index)
        self.slider.blockSignals(False)
        self.update_floatEdit()

    def set_slider_floatedit(self):
        """Method that set the value of the slider and the one of the floatEdit
        according to the axis sent by WAxisManager.
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        """

        if self.axis.name == "angle":
            self.axis_value = self.axis.get_values(unit="°")
            self.unit = "°"
        else:
            self.axis_value = self.axis.get_values()

        self.lf_value.setValue(min(self.axis_value))
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.axis_value) - 1)

    def update(self, axis):
        """Method that will update the WDataExtractor widget according to the axis given to it
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        axis : string
            string with the name of the axis that should set the WDataExtractor widget
        """
        self.axis = axis
        self.unit = axis.unit
        self.set_name(axis.name)
        self.update_layout()
        self.set_slider_floatedit()

    def update_floatEdit(self):
        """Method that set the value of the floatEdit according to the value of the slider
        according to the axis sent by WAxisManager.
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        """
        self.lf_value.blockSignals(True)
        self.lf_value.setValue(self.axis_value[self.slider.value()])
        self.lf_value.blockSignals(False)
        self.refreshNeeded.emit()

    def update_layout(self):
        """Method that update the layout of the WDataExtractor according to the extraction chosen
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        """

        extraction_selected = self.c_type_extraction.currentText()

        if extraction_selected == "slice" or extraction_selected == "slice (fft)":
            self.lf_value.show()
            self.slider.show()
            self.refreshNeeded.emit()
        else:
            self.lf_value.hide()
            self.slider.hide()

        if extraction_selected == "superimpose/filter":
            self.b_action.show()
            self.b_action.setText(extraction_selected)
        else:
            self.b_action.hide()
            self.refreshNeeded.emit()

    def update_slider(self):
        """Method that set the value of the slider according to the value of the floatEdit
        according to the axis sent by WAxisManager.
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        """
        self.slider.blockSignals(True)
        index = argmin(np_abs(self.axis_value - self.lf_value.value()))
        self.slider.setValue(index)
        self.lf_value.setValue(self.axis_value[index])
        self.slider.blockSignals(False)
        self.refreshNeeded.emit()
