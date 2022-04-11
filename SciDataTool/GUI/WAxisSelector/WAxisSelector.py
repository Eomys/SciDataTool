from PySide2.QtWidgets import QWidget

from SciDataTool.GUI.WAxisSelector.Ui_WAxisSelector import Ui_WAxisSelector
from SciDataTool.GUI.WFilter.WFilter import WFilter
from PySide2.QtCore import Signal
from SciDataTool.Functions.Plot import (
    unit_dict,
    norm_name_dict,
    axis_norm_dict,
    axes_dict,
    fft_dict,
    ifft_dict,
)
from SciDataTool.GUI import update_cb_enable
from SciDataTool.Functions.Load.import_class import import_class


class WAxisSelector(Ui_WAxisSelector, QWidget):
    """Widget to select the axis to plot"""

    refreshNeeded = Signal()
    axisChanged = Signal()
    actionChanged = Signal()

    def __init__(self, parent=None, path_to_image=None):
        """Initialize the arguments, linking the buttons and setting up the UI

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
        self.norm_list = None  # List of available normalizations for each axis
        self.indices = None
        self.path_to_image = path_to_image

        self.axis_selected = "None"  # Name of the axis selected (time, angle...)
        self.norm = None  # Name of the unit of the axis (s,m...)
        self.b_filter.setEnabled(False)
        self.current_dialog = None

        self.c_axis.currentTextChanged.connect(self.update_axis)
        self.c_action.currentTextChanged.connect(self.update_action)
        self.c_unit.currentTextChanged.connect(self.update_unit)
        self.b_filter.clicked.connect(self.open_filter)

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

        axis_unit_selected = self.get_axis_selected()

        # Add indices if necessary
        if self.get_current_action_name() == "Filter":
            if self.indices is not None:
                axis_unit_selected += str(self.indices)
            else:
                axis_unit_selected += "[]"

        if self.norm is not None:  # Add normalization
            axis_unit_selected += "{" + self.norm + "}"

        elif axis_unit_selected != "None":  # adding unit
            axis_unit_selected += "{" + self.c_unit.currentText() + "}"

        return axis_unit_selected

    def get_current_action_name(self):
        """Method that return the action currently selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current action selected
        """
        return self.c_action.currentText()

    def get_axis_selected(self):
        """Method that return the name of the axis selected of the WAxisSelector
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the axis selected
        """
        if self.c_axis.currentText() == "None":
            return "None"
        else:
            return self.axis_selected

    def open_filter(self):
        """Open the Filter widget"""
        # Close previous dialog
        if self.current_dialog is not None:
            self.current_dialog.close()
            self.current_dialog.setParent(None)
            self.current_dialog = None

        axis_selected_obj = [
            ax for ax in self.axes_list_obj if ax.name == self.axis_selected
        ][0]

        self.current_dialog = WFilter(
            axis_selected_obj,
            self.indices,
            path_to_image=self.path_to_image,
        )
        self.current_dialog.refreshNeeded.connect(self.update_indices)
        self.current_dialog.show()

    def update_indices(self):
        self.indices = self.current_dialog.indices
        self.refreshNeeded.emit()

    def remove_axis(self, axis_to_remove):
        """Method that remove a given axis from the axis ComboBox.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis_to_remove : string
            name of the axis to remove from c_axis

        """
        # if the axis to remove is wavenumber of freqs then we have to remove angle or time
        if axis_to_remove in ifft_dict:
            axis_to_remove = ifft_dict[axis_to_remove]

        if axis_to_remove in self.axes_list:
            axes_list = self.axes_list[:]  # Getting the axes available
            axes_list.remove(axis_to_remove)  # Removing the axis selected

            # Building the new ComboBox
            self.c_axis.blockSignals(True)
            self.c_axis.clear()

            for ax in axes_list:
                if ax in axes_dict:
                    self.c_axis.addItem(axes_dict[ax])
                else:
                    self.c_axis.addItem(ax)

            update_cb_enable(self.c_axis)
            self.c_axis.blockSignals(False)

            self.update_axis(is_refresh=False)

    def set_axis(self, axis):
        """Method that will set the comboboxes to have the axis given as an input when calling the plot method (auto-plot).
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis : RequestedAxis
            axis that we want to have in the WAxisSelector
        """
        self.blockSignals(True)
        self.indices = axis.indices
        # Step 1 : Getting the name of the axis and selecting the right combobox (axis and action)
        axis_name = axis.name

        # If the axis is freqs or wavenumber, then we have to select time/angle and fft
        if axis_name in ifft_dict:
            # Selecting the right axis
            self.c_axis.setCurrentIndex(self.c_axis.findText(ifft_dict[axis_name]))
            # Making sure that we select FFT
            self.c_action.setCurrentIndex(1)
        else:
            # Selecting the right axis
            if axis_name in axes_dict:
                self.c_axis.setCurrentIndex(self.c_axis.findText(axes_dict[axis_name]))
            else:
                self.c_axis.setCurrentIndex(self.c_axis.findText(axis_name))

        # Step 2 : Recovering the unit and setting the combobox according to it
        unit_name = axis.unit
        self.c_unit.blockSignals(True)
        if self.c_unit.findText(unit_name) != -1:
            self.c_unit.setCurrentIndex(self.c_unit.findText(unit_name))
        elif unit_name in unit_dict:
            self.c_unit.setCurrentIndex(self.c_unit.findText(unit_dict[unit_name]))
        elif unit_name in norm_name_dict:
            self.c_unit.setCurrentIndex(self.c_unit.findText(norm_name_dict[unit_name]))
        elif unit_name == "SI":
            self.c_unit.setCurrentIndex(0)
        else:
            self.c_unit.setCurrentIndex(self.c_unit.findText(unit_name))
        self.c_unit.blockSignals(False)
        self.set_unit()

        self.blockSignals(False)

    def set_axis_options(self, axes_list):
        """Method that will put the axes of data in the combobox of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axes_list : list
            A list of axis object from the Data object that we want to plot

        """
        # Dynamic import to avoid import loop
        DataPattern = import_class("SciDataTool.Classes", "DataPattern")

        self.c_axis.blockSignals(True)
        # Step 1 : Getting the name of the different axes of the DataND object
        self.axes_list = [
            axis.name
            for axis in axes_list
            if axis.is_overlay == False
            and not (isinstance(axis, DataPattern) and len(axis.unique_indices) == 1)
        ]  # Remove overlay axes + slice axes with single slice
        self.norm_list = [
            list(axis.normalizations.keys())
            for axis in axes_list
            if axis.is_overlay == False
            and not (isinstance(axis, DataPattern) and len(axis.unique_indices) == 1)
        ]

        # Adding a safety, so that we cannot have frequency or wavenumber inside axes_list (we should have time and angle instead)
        for i in range(len(self.axes_list)):
            if self.axes_list[i] in ifft_dict:
                self.axes_list[i] = ifft_dict[self.axes_list[i]]

        # At least one axis must be selected => impossible to have none for X axis
        if self.name.lower() != "x":
            self.axes_list.insert(0, "None")
            self.norm_list.insert(0, None)

        # Step 2 : Replacing the items inside of the ComboBox with the axes recovered
        self.c_axis.clear()
        for ax in self.axes_list:
            if ax in ifft_dict:
                self.c_axis.addItem(ifft_dict[ax])
            else:
                if ax in axes_dict:
                    self.c_axis.addItem(axes_dict[ax])
                else:
                    self.c_axis.addItem(ax)

        update_cb_enable(self.c_axis)
        self.c_axis.blockSignals(False)

        # Step 3 : Modifying axis_selected
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            self.axis_selected = [key for key in axes_dict][
                [axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())
            ]
        else:
            self.axis_selected = self.c_axis.currentText()

        self.c_axis.view().setMinimumWidth(max([len(ax) for ax in self.axes_list]) * 6)

        if self.c_axis.currentText() == "None":
            self.c_action.setDisabled(True)
        else:
            self.c_action.setDisabled(False)

    def set_name(self, axis_name):
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

    def set_action(self, action):
        """Method that set the action of the WAxisSelector
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        action : string
            name of the new action"""

        action_list = [self.c_action.itemText(i) for i in range(self.c_action.count())]
        self.c_action.blockSignals(True)
        if action in action_list and action != "Filter":
            self.c_action.setCurrentIndex(action_list.index(action))
        self.c_action.blockSignals(False)

    def set_unit(self):
        """Method that update the unit comboxbox according to the axis selected in the other combobox.
           We can also give the axis selected and put its units inside the combobox
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        """
        self.c_unit.blockSignals(True)
        # Adding the right units according to a dictionnary
        if self.axis_selected == "None":
            # If the axis is not selected, then we can not choose the unit
            self.c_unit.clear()
            self.c_unit.setDisabled(True)
        else:
            self.c_unit.setDisabled(False)
            self.c_unit.clear()

            # Adding the axis unit + available normalizations
            if self.axis_selected in unit_dict:
                self.c_unit.addItem(unit_dict[self.axis_selected])
            norms = self.norm_list[self.axes_list.index(self.axis_selected)]
            norm_id = None
            if norms is not None:
                for norm in norms:
                    if norm in axis_norm_dict[self.axis_selected]:
                        self.c_unit.addItem(norm_name_dict[norm])  # Add longer names
                        if "_id" in norm:
                            norm_id = norm_name_dict[norm]

            # Use tooth index as only normalization
            if norm_id is not None:
                self.c_unit.clear()
                self.c_unit.addItem(norm_id)

            # Modifying the size of the list according to the units available (adapting it when normalization)
            cb_width = 0
            for idx_unit in range(self.c_unit.count()):
                self.c_unit.setCurrentIndex(idx_unit)
                if len(self.c_unit.currentText()) > cb_width:
                    cb_width = len(self.c_unit.currentText())
            self.c_unit.setCurrentIndex(0)

            self.c_unit.view().setMinimumWidth(cb_width * 8)

        update_cb_enable(self.c_unit)
        self.c_unit.blockSignals(False)
        self.update_unit()

    def update(self, axes_list, axis_name="X"):
        """Method used to update the widget by calling the other method for the label, the axes and the units
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axes_list : list
            A list of axis object from the Data object that we want to plot
        axis_name : string
            string that will set the text of in_name (=name of the axis)
        """
        self.axes_list_obj = axes_list
        self.set_name(axis_name)
        self.set_axis_options(axes_list)
        self.update_axis()
        self.set_unit()

    def update_axis(self, text=None, is_refresh=True):
        """Method called when an axis is changed that change axis_selected, the units available and the action combobox.
        It will also emit a signal used in WAxisManager.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        """
        self.c_action.blockSignals(True)
        if is_refresh:
            self.c_action.setCurrentIndex(0)

        if self.c_axis.currentText() == "None":
            self.c_action.setDisabled(True)
        else:
            self.c_action.setDisabled(False)

        # Updating the units and the axis selected
        # Making sure that self.axis_selected is a "tag" and not a "label". Example : z instead of axial direction
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            self.axis_selected = [key for key in axes_dict][
                [axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())
            ]
        else:
            self.axis_selected = self.c_axis.currentText()

        if not is_refresh:
            self.set_unit()

        # Updating the action combobox
        # Handling specific case to disable certain parts of the GUI
        if self.c_axis.currentText() == "None":
            self.c_action.setDisabled(True)
        else:
            self.c_action.setDisabled(False)

        if self.axis_selected in fft_dict:
            action = ["None", "FFT"]
        elif (
            self.axis_selected in [axis.name for axis in self.axes_list_obj]
            and self.axes_list_obj[
                [axis.name for axis in self.axes_list_obj].index(self.axis_selected)
            ].is_components
        ):
            action = ["None", "Filter"]
        else:
            action = ["None"]
        self.c_action.clear()
        self.c_action.addItems(action)
        update_cb_enable(self.c_action)
        self.c_action.blockSignals(False)

        self.c_action.view().setMinimumWidth(max([len(ac) for ac in action]) * 6)

        if "Filter" in action:
            self.b_filter.show()
        else:
            sp_retain = self.b_filter.sizePolicy()
            sp_retain.setRetainSizeWhenHidden(True)
            self.b_filter.setSizePolicy(sp_retain)
            self.b_filter.hide()

        # Emitting the signals
        if is_refresh:
            self.refreshNeeded.emit()
            self.axisChanged.emit()

    def update_action(self):
        """Method called when an action is changed that will change axis_selected,
        update the units available and emit a signal.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        # If the action selected is filter, then we enable the button
        if self.c_action.currentText() == "Filter":
            self.b_filter.setEnabled(True)

        else:
            self.b_filter.setEnabled(False)

        # Converting the axes according to action selected if possible/necessary
        if self.c_action.currentText() == "FFT" and self.axis_selected in fft_dict:
            self.axes_list.insert(
                self.axes_list.index(self.axis_selected), fft_dict[self.axis_selected]
            )
            self.axes_list.remove(self.axis_selected)
            self.axis_selected = fft_dict[self.axis_selected]

        elif self.c_action.currentText() == "None" and self.axis_selected in ifft_dict:
            self.axes_list.insert(
                self.axes_list.index(self.axis_selected), ifft_dict[self.axis_selected]
            )
            self.axes_list.remove(self.axis_selected)
            self.axis_selected = ifft_dict[self.axis_selected]

        # Handling the case where axis_selected is updated but axes_list is not
        # We check if fft(axis_selected) is in the list and when it is the case we replace it by axis_selected
        if not self.axis_selected in self.axes_list:
            if fft_dict[self.axis_selected] in self.axes_list:
                self.axes_list.insert(
                    self.axes_list.index(fft_dict[self.axis_selected]),
                    self.axis_selected,
                )
                self.axes_list.remove(fft_dict[self.axis_selected])

        # Now that the quantiy has been updated according to the action, we can set the units and emit the signals
        self.set_unit()

        self.refreshNeeded.emit()
        self.actionChanged.emit()

    def update_unit(self):
        """Method called when a new unit is selected so that we can update self.norm
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        normalization = self.c_unit.currentText()
        is_match = False
        # Replace normalization title with normalization name
        for norm in norm_name_dict:
            if normalization == norm_name_dict[norm]:
                self.norm = norm
                is_match = True
        if not is_match:
            self.norm = None

        self.refreshNeeded.emit()
