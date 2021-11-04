from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QSpacerItem, QWidget
from PySide2.QtCore import Signal

from SciDataTool.GUI.WAxisSelector.WAxisSelector import WAxisSelector

from ...GUI.WAxisManager.Ui_WAxisManager import Ui_WAxisManager
from ...GUI.WDataExtractor.WDataExtractor import WDataExtractor
from ...Functions.Plot import fft_dict, ifft_dict, axes_dict


EXTENSION_DICT = {
    "slice": ["rss", "sum", "rms", "mean", "integrate", "list", "single"],
    "axis": [
        "derivate",
        "oneperiod",
        "antiperiod",
        "smallestperiod",
        "pattern",
        "axis_data",
        "interval",
        "whole",
    ],
}


class WAxisManager(Ui_WAxisManager, QWidget):
    """Widget that will handle the selection of the axis as well as generating WDataExtractor"""

    refreshNeeded = Signal()
    refreshRange = Signal()

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.axes_list = list()

        # Managing the signal emitted by the WAxisSelector widgets
        self.w_axis_1.axisChanged.connect(self.axis_1_updated)
        self.w_axis_2.axisChanged.connect(self.axis_2_updated)

        # The operation in axis 2 is by default the one chosen in axis 1
        self.w_axis_1.operationChanged.connect(self.operation_sync)

    def axis_1_updated(self):
        """Method that remove the axis selected in w_axis_1 from the the other WAxisSelector widget and generates Data Selection
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """
        # Making sure that when axis 1 is updated, axis 1 and 2 are both on "" for the operation combobox
        self.operation_sync()

        # Recovering the axis selected by the user
        axis_selected = self.w_axis_1.get_current_axis_name()

        # Removing the axis selected from the the second axis combobox
        self.w_axis_2.remove_axis(axis_selected)

        # Generating the DataSelection GroupBox
        self.gen_data_selec()

    def axis_2_updated(self):
        """Method that make sure that when axis 2 is selected (None->?) it has the same operation as axis1 then generates Data Selection
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """
        # Making sure that when axis 1 is updated, axis 1 and 2 are both on "" for the operation combobox
        self.operation_sync()

        # Generating the DataSelection GroupBox
        self.gen_data_selec()

    def gen_data_selec(self):
        """Method that gen the right WDataExtrator widget according to the axis selected by the user in the UI
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """

        # Step 1 : Recovering the axis to generate (those that are not selected)
        # Getting all the possible axes
        axes_list_1 = self.w_axis_1.get_axes_name()[:]
        axes_list_2 = self.w_axis_2.get_axes_name()[:]

        # Getting the axes selected and removing them from the right axes_list
        axis_selected_1 = self.w_axis_1.get_current_quantity()
        axis_selected_2 = self.w_axis_2.get_current_quantity()

        axes_list_1.remove(axis_selected_1)
        axes_list_2.remove(axis_selected_2)

        # Selecting the axes that are in common between the two axes lists
        axes_gen = [ax for ax in axes_list_1 if ax in axes_list_2]

        # Step 2 : Removing the items that are in the layout currently
        for i in reversed(range(self.lay_data_extract.count())):
            if not isinstance(self.lay_data_extract.itemAt(i), QSpacerItem):
                self.lay_data_extract.takeAt(i).widget().deleteLater()

        # Step  3 : Adding a WDataExtractor widget for each axis inside the layout
        self.w_data_sel = list()

        for axis in axes_gen:
            temp = WDataExtractor(self.layoutWidget)
            temp.setObjectName(axis)
            for ax in self.axes_list:
                if ax.name == axis:
                    temp.update(ax)
            self.w_data_sel.append(temp)

        for wid in self.w_data_sel:
            self.lay_data_extract.insertWidget(self.lay_data_extract.count() - 1, wid)
            wid.refreshNeeded.connect(self.updateNeeded)

        self.updateNeeded()

    def get_axes_selected(self):
        """Method that return the axes chosen by the user and their unit as a string
        so that we can use them to plot the data.
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        Output
        ---------
        string
            name of the axis and their units
        """

        axes_selected = list()

        # Recovering the first axis
        axes_selected.append(self.w_axis_1.get_axis_unit_selected())

        # If a second axis is selected, then we add it as well
        if self.w_axis_2.get_current_quantity() != "None":
            axes_selected.append(self.w_axis_2.get_axis_unit_selected())

        return axes_selected

    def get_dataselection_action(self):
        """Method that return the actions chosen by the user and the related axe as a string
         so that we can use them to plot the data.
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        Output
        ---------
        string
            name of the action and its axis
        """

        actions_selected = list()
        for widget in self.w_data_sel:
            actions_selected.append(widget.get_actionSelected())

        return actions_selected

    def operation_sync(self):
        """Method that will check the operation chosen and that update the other operation combobox to have the same operation.
        So that, by default, we have FFT and FFT or "" and ""
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object

        """

        operation_selected = self.w_axis_1.get_current_operation_name()
        self.w_axis_2.set_operation(operation_selected)
        self.gen_data_selec()

    def set_axes(self, data, user_input_list):
        """Method used to set the axes of the Axes group box as well as setting the widgets of the DataSelection groupbox
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            The DataND object that we want to plot
        """

        # Step 1 : If setting are given, we have to process them
        axes_list = list()
        slices_op_list = list()

        for axis in user_input_list:
            if axis.extension in EXTENSION_DICT["axis"]:
                axes_list.append(axis)

            elif axis.extension in EXTENSION_DICT["slice"]:
                slices_op_list.append(axis)

        # Step 2 : Setting the UI according to def setting if we have user input or by default if there are not user input

        if len(user_input_list) == 0:

            self.w_axis_1.blockSignals(True)
            self.w_axis_2.blockSignals(True)

            self.w_axis_1.update(data)
            self.w_axis_2.update(data, axis_name="Y")
            self.axes_list = data.get_axes()
            self.axis_1_updated()

            self.w_axis_1.blockSignals(False)
            self.w_axis_2.blockSignals(False)

        else:
            self.w_axis_1.blockSignals(True)
            self.w_axis_2.blockSignals(True)

            self.w_axis_1.update(data)
            self.w_axis_1.set_axis_default(axes_list[0])

            self.w_axis_2.update(data, axis_name="Y")
            self.axes_list = data.get_axes()
            self.axis_1_updated()

            if len(axes_list) == 2:
                self.w_axis_2.set_axis_default(axes_list[1])

            self.axis_2_updated()

            self.set_data_selec(slices_op_list)

            self.w_axis_1.blockSignals(False)
            self.w_axis_2.blockSignals(False)

    def set_data_selec(self, user_input_list):

        for wid in self.w_data_sel:
            wid.set_op(user_input_list[self.w_data_sel.index(wid)])

    def updateNeeded(self):
        """Method that emits a signal that will be used to automaticaly update the plot inside the GUI.
        This signal is triggered by other signals comming from WDataExtractor or WAxisSelector.
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """

        self.refreshNeeded.emit()
        self.refreshRange.emit()
