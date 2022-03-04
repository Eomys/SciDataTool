from PySide2.QtWidgets import QWidget

from SciDataTool.GUI.WSliceOperator.Ui_WSliceOperator import Ui_WSliceOperator
from SciDataTool.GUI.WFilter.WFilter import WFilter
from PySide2.QtCore import Signal
from SciDataTool.Functions.Plot import axes_dict, fft_dict, ifft_dict, unit_dict
from SciDataTool.Classes.Data import Data
from numpy import where
from numpy import argmin, abs as np_abs

type_extraction_dict = {
    "max": "=max",
    "min": "=min",
    "rms": "=rms",
    "rss": "=rss",
    "sum": "=sum",
    "mean": "=mean",
}

OPERATION_LIST = [
    "slice",
    "slice (fft)",
    "max",
    "min",
    "rms",
    "rss",
    "sum",
    "mean",
    "overlay",
]


class WSliceOperator(Ui_WSliceOperator, QWidget):
    """Widget to define how to handle the 'non-plot' axis"""

    refreshNeeded = Signal()

    def __init__(self, parent=None):
        """Initialize the GUI according to info given by the WAxisManager widget

        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        parent : QWidget
            The parent QWidget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.name = "angle"
        self.axis = Data
        self.current_dialog = None
        self.indices = None

        self.c_operation.currentTextChanged.connect(self.update_layout)
        self.slider.valueChanged.connect(self.update_floatEdit)
        self.lf_value.editingFinished.connect(self.update_slider)
        self.b_action.clicked.connect(self.open_filter)

    def get_operation_selected(self):
        """Method that return a string of the action selected by the user on the axis of the widget.
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object

        Output
        ---------
        string
            name of the current action selected
        """
        # Recovering the action selected by the user
        action_type = self.c_operation.currentText().split(" over")[0]

        # Formatting the string to have the right syntax
        if action_type == "slice":
            # slice_index = self.slider.value()
            # action = "[" + str(slice_index) + "]"
            action = "=" + str(self.lf_value.value())
            return self.axis_name + action + "{" + self.unit + "}"

        elif action_type == "slice (fft)":
            # slice_index = self.slider.value()
            # action = "[" + str(slice_index) + "]"
            action = "=" + str(self.lf_value.value())
            if self.axis_name in fft_dict:
                return fft_dict[self.axis_name] + action

        elif action_type == "overlay":
            if self.indices is None:
                return self.axis_name + "[]"
            else:
                return self.axis_name + str(self.indices)

        elif action_type in type_extraction_dict:
            action = type_extraction_dict[action_type]
            return self.axis_name + action + "{" + self.unit + "}"
        else:
            return None

    def get_name(self):
        """Method that return the name of the axis of the WSliceOperator
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        """
        return self.name

    def open_filter(self):
        """Open the Filter widget"""
        # Close previous dialog
        if self.current_dialog is not None:
            self.current_dialog.close()
            self.current_dialog.setParent(None)
            self.current_dialog = None

        self.current_dialog = WFilter(self.axis, self.indices)
        self.current_dialog.refreshNeeded.connect(self.update_indices)
        self.current_dialog.show()

    def update_indices(self):
        self.indices = self.current_dialog.indices
        self.refreshNeeded.emit()

    def set_name(self, name):
        """Method that set the name of the axis of the WSliceOperator
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        name : string
            string that hold the name of the axis
        """
        # Checking if the name of the axis is the name as the one displayed (z =/= axial direction for example)
        if name in axes_dict:
            self.in_name.setText(axes_dict[name])
        else:
            self.in_name.setText(name)

        self.name = name

    def set_operation(self, user_input):
        """Method that set the operation of the combobox of the WSliceOperator
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        user_input : list
            list of RequestedAxis that we use to set up the UI for the auto-plot
        """
        # Recovering the type of the operation and on which axis we are applying it
        operation_type = user_input.extension
        operation_name = user_input.name

        # Setting the label of the widget with the right name
        self.set_name(operation_name)

        # Converting type of the operation if we have a slice or an overlay
        if operation_type == "single":
            operation_type = "slice"

        elif operation_type == "list":
            operation_type = "overlay"

        else:
            operation_type += " over " + self.name

        # Setting operation combobox to the right operation
        self.c_operation.setCurrentIndex(self.c_operation.findText(operation_type))

        # Setting the slider to the right value if the operation is slice
        if operation_type == "slice":
            if user_input.indices is None:
                index = 0
            else:
                index = user_input.indices[0]
            self.set_slider(index)

    def set_slider(self, index):
        """Method that set the value of the slider of the WSliceOperator and then update floatEdit
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        index : int
            index at which the slider should be placed
        """
        self.slider.blockSignals(True)
        if index >= 0:
            self.slider.setValue(index)
        else:
            self.slider.setValue(self.slider.maximum() + index)
        self.slider.blockSignals(False)
        self.update_floatEdit()

    def set_slider_floatedit(self):
        """Method that set the value of the slider and the one of the floatEdit
        according to the axis sent by WAxisManager.
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        """
        if not self.axis.is_components:
            # Converting the axis from rad to degree if the axis is angle as we do slice in degrees
            # Recovering the value from the axis as well
            if self.c_operation.currentText() == "slice":
                if self.axis.name in ifft_dict:
                    operation = self.axis.name + "_to_" + self.axis_name
                else:
                    operation = None
                if self.axis_name in ifft_dict:
                    name = ifft_dict[self.axis_name]
                else:
                    name = self.axis_name
                self.set_name(name)
                if self.axis_name == "angle":
                    self.axis_value = self.axis.get_values(
                        unit="°", operation=operation, corr_unit="rad", is_full=True
                    )
                    self.unit = "°"
                else:
                    self.axis_value = self.axis.get_values(
                        operation=operation, is_full=True
                    )
            elif self.c_operation.currentText() == "slice (fft)":
                if self.axis_name in fft_dict:
                    name = fft_dict[self.axis_name]
                else:
                    name = self.axis_name
                self.set_name(name)
                if self.axis.name == "angle":
                    self.axis_value = self.axis.get_values(
                        operation="angle_to_wavenumber"
                    )
                    self.unit = ""
                elif self.axis.name == "time":
                    self.axis_value = self.axis.get_values(operation="time_to_freqs")
                    self.unit = "Hz"
                else:  # already wavenumber of freqs case
                    self.axis_value = self.axis.get_values()

            # Setting the initial value of the floatEdit to the minimum inside the axis
            self.lf_value.setValue(min(self.axis_value))

            # Setting the axis unit
            if name in unit_dict:
                self.unit = unit_dict[name]
            self.in_unit.setText("[" + self.unit + "]")

            # Setting the slider by giving the number of index according to the size of the axis
            self.slider.setMinimum(0)
            self.slider.setMaximum(len(self.axis_value) - 1)
            self.slider.setValue(0)

    def update(self, axis, axis_request=None):
        """Method that will update the WSliceOperator widget according to the axis given to it
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        axis : string
            string with the name of the axis that should set the WSliceOperator widget
        """
        self.axis = axis
        if axis_request is not None:
            axis_request.corr_unit = axis_request.unit
            axis_request.get_axis(axis, True)
            self.indices = axis_request.indices
        self.unit = axis.unit
        if axis.name in ifft_dict:  # DataFreq case
            self.axis_name = ifft_dict[axis.name]
        else:
            self.axis_name = axis.name
        self.set_name(self.axis_name)

        self.c_operation.blockSignals(True)
        operation_list = [
            ope + " over " + self.name if ope in type_extraction_dict else ope
            for ope in OPERATION_LIST
        ]

        # Remove slice for string axes
        if self.axis.is_components:
            operation_list.remove("slice")
        else:
            self.set_slider_floatedit()

        # Remove overlay for non is_components axes
        if not self.axis.is_components:
            operation_list.remove("overlay")

        # Remove fft slice for non fft axes
        if not self.axis_name in fft_dict:
            operation_list.remove("slice (fft)")

        self.c_operation.clear()
        self.c_operation.addItems(operation_list)
        self.update_layout()
        if self.axis.is_overlay:
            self.c_operation.setCurrentIndex(operation_list.index("overlay"))
            self.b_action.show()
            self.b_action.setText("Overlay")
        self.c_operation.blockSignals(False)

    def update_floatEdit(self, is_refresh=True):
        """Method that set the value of the floatEdit according to the value returned by the slider
        and the axis sent by WAxisManager.
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        """

        self.lf_value.blockSignals(True)

        self.lf_value.setValue(self.axis_value[self.slider.value()])

        self.lf_value.blockSignals(False)
        if is_refresh:
            self.refreshNeeded.emit()

    def update_layout(self):
        """Method that update the layout of the WSliceOperator according to the extraction chosen
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        """
        # Recovering the operation selected
        extraction_selected = self.c_operation.currentText().split(" over")[0]

        # If the operation selected is a slice, then we show the slider and the floatEdit
        if extraction_selected == "slice" or extraction_selected == "slice (fft)":
            self.set_slider_floatedit()
            self.lf_value.show()
            self.in_unit.show()
            self.slider.show()
            self.b_action.hide()
            self.refreshNeeded.emit()
        # If the operation selected is overlay then we show the related button
        elif extraction_selected == "overlay":
            self.lf_value.hide()
            self.in_unit.hide()
            self.slider.hide()
            self.b_action.show()
            self.b_action.setText("Overlay")
            self.refreshNeeded.emit()
        else:
            self.lf_value.hide()
            self.in_unit.hide()
            self.slider.hide()
            self.b_action.hide()
            self.refreshNeeded.emit()

    def update_slider(self):
        """Method that set the value of the slider according to the value of the floatEdit
        according to the axis sent by WAxisManager.
        Parameters
        ----------
        self : WSliceOperator
            a WSliceOperator object
        """

        self.slider.blockSignals(True)
        # We set the value of the slider to the index closest to the value given
        index = argmin(np_abs(self.axis_value - self.lf_value.value()))
        self.slider.setValue(index)
        # We update the value of floatEdit to the index selected
        self.lf_value.setValue(self.axis_value[index])
        self.slider.blockSignals(False)
        self.refreshNeeded.emit()
