from PySide2.QtWidgets import QWidget

from ...GUI.WAxisSelector.Ui_WAxisSelector import Ui_WAxisSelector
from PySide2.QtCore import Signal
from ...Functions.Plot import unit_dict, axes_dict, fft_dict, ifft_dict


class WAxisSelector(Ui_WAxisSelector, QWidget):
    """Widget to select the axis to plot"""

    refreshNeeded = Signal()
    axisChanged = Signal()
    operationChanged = Signal()

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = "X"  # Name of the axis
        self.axes_list = list()  # List of the different axes of the DataND object

        self.quantity = "None"  # Name of the quantity of the axis (time, angle...)
        self.unit = "None"  # Name of the unit of the axis (s,m...)
        self.b_filter.setDisabled(True)

        self.c_axis.currentTextChanged.connect(self.update_axis)
        self.c_operation.currentTextChanged.connect(self.update_operation)
        self.c_unit.currentTextChanged.connect(self.update_unit)

    def set_axis_default(self, axis):
        """Method that will set the comboboxes to have the axis given as an input when calling the plot method.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis : RequestedAxis
            axis that we want to have in the WAxisSelector
        """
        # Step 1 : Getting the name of the axis and selecting the right combobox (axis and operation)

        self.c_axis.blockSignals(True)
        self.c_operation.blockSignals(True)

        axis_name = axis.name

        # If the axis is freqs or wavenumber, then we have to select time/angle and fft
        if axis_name in ifft_dict:

            # Selecting the right axis
            for i in range(self.c_axis.count()):
                self.c_axis.setCurrentIndex(i)
                if self.c_axis.currentText() == ifft_dict[axis_name]:
                    break

            self.update_axis(emit_signal=False)

            # Making sure that we select FFT
            self.c_operation.setCurrentIndex(1)

        else:
            # Selecting the right axis
            for i in range(self.c_axis.count()):
                self.c_axis.setCurrentIndex(i)
                if self.c_axis.currentText() == axis_name:
                    break

            self.update_axis(emit_signal=False)

        self.c_axis.blockSignals(False)
        self.c_operation.blockSignals(False)

        self.blockSignals(True)
        self.update_operation()
        self.blockSignals(False)

        # Step 2 : Recovering the unit and setting the combobox according to it
        self.c_unit.blockSignals(True)
        unit_name = axis.unit

        if unit_name in unit_dict:
            for i in range(self.c_unit.count()):
                self.c_unit.setCurrentIndex(i)
                if self.c_unit.currentText() == unit_name:
                    break

        self.c_unit.blockSignals(False)
        self.update_unit()

    def change_name(self, axis_name):
        """Method to change of the label of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis_name : string
            string that we will use to set the in_name of the widget

        """

        self.name = axis_name
        self.in_name.setText(axis_name)

    def get_axes_name(self):
        """Method that return the axes that can be selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        list
            name of the axes avalaible
        """
        return self.axes_list

    def get_axis_unit_selected(self):
        """Method that return the axis and the unit currently selected so that we can use it in the plot method
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current axis and unit selected in the right format
        """

        return self.quantity + "{" + self.unit + "}"

    def get_current_axis_name(self):
        """Method that return the axis currently selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current axis selected
        """
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            return [key for key in axes_dict][
                [axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())
            ]
        else:
            return self.c_axis.currentText()

    def get_current_operation_name(self):
        """Method that return the operation currently selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current operation selected
        """
        return self.c_operation.currentText()

    def get_current_quantity(self):
        """Method that return the name of the quantity of the WAxisSelector
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the quantity
        """
        return self.quantity

    def get_current_unit(self):
        """Method that return the unit currently selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current unit selected
        """

        return self.unit

    def remove_axis(self, axis_to_remove):
        """Method that remove a given axis from the axis ComboBox.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis_to_remove : string
            name of the axis to remove from c_axis

        """
        if axis_to_remove in self.axes_list:
            axes_list = self.axes_list[:]  # Getting the axes available
            axes_list.remove(axis_to_remove)  # Removing the axis seleted

            # Building the new ComboBox
            self.c_axis.blockSignals(True)
            self.c_axis.clear()
            for i in range(len(axes_list)):
                if axes_list[i] in axes_dict:
                    self.c_axis.addItem(axes_dict[axes_list[i]])
                else:
                    self.c_axis.addItem(axes_list[i])
            self.c_axis.blockSignals(False)

            self.update_axis()

    def set_axis(self, data):
        """Method that will put the axes of data in the combobox of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        data : DataND
            A DataND object that we want to plot

        """
        self.c_axis.blockSignals(True)
        # Step 1 : Getting the name of the different axes of the DataND object
        self.axes_list += [axis.name for axis in data.get_axes()]

        # At least one axis must be selected => impossible to have none for X axis
        if self.name.lower() != "x":
            self.axes_list.insert(0, "None")

        # Step 2 : Replacing the items inside of the ComboBox with the axes recovered
        self.c_axis.clear()
        for i in range(len(self.axes_list)):
            if self.axes_list[i] in axes_dict:
                self.c_axis.addItem(axes_dict[self.axes_list[i]])
            else:
                self.c_axis.addItem(self.axes_list[i])

        self.c_axis.blockSignals(False)

        # Step 3 : Modifying quantity
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            self.quantity = [key for key in axes_dict][
                [axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())
            ]
        else:
            self.quantity = self.c_axis.currentText()

    def set_operation(self, operation):
        """Method that set the operation of the WAxisSelector
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        operation : string
            name of the new operation"""

        operation_list = [
            self.c_operation.itemText(i) for i in range(self.c_operation.count())
        ]

        if operation in operation_list and operation != "Filter":
            self.c_operation.setCurrentIndex(operation_list.index(operation))

    def set_unit(self):
        """Method that update the unit comboxbox according to the axis selected in the other combobox.
           We can also give the axis selected and put its units inside the combobox
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis : string
            name of the axis that is selected
        """
        self.c_unit.blockSignals(True)
        # Adding the right units according to a dictionnary
        if self.quantity == "None":
            # If the axis is not selected, then we can not choose the unit
            self.c_unit.clear()
            self.c_unit.setDisabled(True)
        else:
            self.c_unit.setDisabled(False)
            self.c_unit.clear()

            # Adding the right unit according to the imported dictionary
            if self.quantity in unit_dict:
                self.c_unit.addItems(unit_dict[self.quantity])
        self.c_unit.blockSignals(False)
        self.update_unit()

    def update(self, data, axis_name="X"):
        """Method used to update the widget by calling the other method for the label, the axes and the units
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        data : DataND
            A DataND object to plot
        axis_name : string
            string that will set the text of in_name (=name of the axis)
        """

        self.change_name(axis_name)
        self.set_axis(data)
        self.set_unit()

    def update_axis(self, emit_signal=True):
        """Method called when an axis is changed that change the quantity, the units available and the operation combobox.
        It will also emit a signal used in WAxisManager.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        """
        self.blockSignals(True)
        self.c_operation.setCurrentIndex(0)

        # Updating the units and the quantity selected
        # Making sure that self.quantity is a "tag" and not a "label". Example : z instead of axial direction
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            self.quantity = [key for key in axes_dict][
                [axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())
            ]
        else:
            self.quantity = self.c_axis.currentText()

        self.set_unit()

        # Updating the operation combobox
        # Handling specific case to disable certain parts of the GUI
        if self.c_axis.currentText() == "None":
            self.c_operation.setDisabled(True)
        else:
            self.c_operation.setDisabled(False)

        if self.quantity in fft_dict:
            operation = ["", "FFT", "Filter"]
            self.c_operation.clear()
            self.c_operation.addItems(operation)

        else:
            operation = ["", "Filter"]
            self.c_operation.clear()
            self.c_operation.addItems(operation)

        self.blockSignals(False)

        # Emitting the signals
        if emit_signal:
            self.refreshNeeded.emit()
            self.axisChanged.emit()

    def update_operation(self):
        """Method called when an operation is changed that will change the quantity of the axis,
        update the units available and emit a signal
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        # If the operation selected is filter, then we enable the button
        if self.c_operation.currentText() == "Filter":
            self.b_filter.setDisabled(False)

        else:
            self.b_filter.setDisabled(True)

        # Converting the axes according to operation selected if possible
        if self.c_operation.currentText() == "FFT" and self.quantity in fft_dict:
            self.axes_list.insert(
                self.axes_list.index(self.quantity), fft_dict[self.quantity]
            )
            self.axes_list.remove(self.quantity)
            self.quantity = fft_dict[self.quantity]

        elif self.c_operation.currentText() == "" and self.quantity in ifft_dict:
            self.axes_list.insert(
                self.axes_list.index(self.quantity), ifft_dict[self.quantity]
            )
            self.axes_list.remove(self.quantity)
            self.quantity = ifft_dict[self.quantity]

        # Handling the case where quantity is updated but axes_list is not
        # We check if fft(quantity) is in the list and when it is the case we replace it by quantity
        if not self.quantity in self.axes_list:
            if fft_dict[self.quantity] in self.axes_list:
                self.axes_list.insert(
                    self.axes_list.index(fft_dict[self.quantity]), self.quantity
                )
                self.axes_list.remove(fft_dict[self.quantity])

        # Now that the quantiy has been updated according to the operation, we can set the units and emit the signals
        self.set_unit()

        self.refreshNeeded.emit()
        self.operationChanged.emit()

    def update_unit(self):
        """Method called when a new unit is selected so that we can update self.unit
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        self.unit = self.c_unit.currentText()
