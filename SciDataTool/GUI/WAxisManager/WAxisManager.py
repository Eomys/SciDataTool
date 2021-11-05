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
        self.w_axis_1.operationChanged.connect(self.fft_sync)

    def axis_1_updated(self):
        """Method that remove the axis selected in w_axis_1 from w_axis_2 and call the method that generates
        the layout with the WDataExtractor.
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """
        # Making sure that when axis 1 is updated, axis 1 and 2 are both on "" for the operation combobox
        self.fft_sync()

        # Recovering the axis selected by the user removing it from the the second axis combobox
        self.w_axis_2.remove_axis(self.w_axis_1.get_current_axis_name())

        # Generating the GroupBox
        self.gen_data_selection()

    def axis_2_updated(self):
        """Method that make sure that when axis 2 is selected (None->?) it has the same fft/ifft combobox selected as axis1
         then generates Data Selection
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """
        # Making sure that when axis 1 is updated, axis 1 and 2 are both on "" for the operation combobox
        self.fft_sync()

        # Generating the DataSelection GroupBox
        self.gen_data_selection()

    def gen_data_selection(self):
        """Method that gen the right WDataExtrator widget according to the axis selected by the user in the UI
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """

        # Step 1 : Recovering the axis that must be generated (those that are not selected)
        # Getting all the possible axes
        axes_list_1 = self.w_axis_1.get_axes_name()[:]
        axes_list_2 = self.w_axis_2.get_axes_name()[:]

        # Getting the axes selected and removing them from the right axes_list
        axis_selected_1 = self.w_axis_1.get_current_axis_selected()
        axis_selected_2 = self.w_axis_2.get_current_axis_selected()

        axes_list_1.remove(axis_selected_1)
        axes_list_2.remove(axis_selected_2)

        # Selecting the axes that are in common between the two axes lists
        axes_gen = [ax for ax in axes_list_1 if ax in axes_list_2]

        # Step 2 : Removing the items that are in the layout currently
        for i in reversed(range(self.lay_data_extract.count())):
            if not isinstance(self.lay_data_extract.itemAt(i), QSpacerItem):
                self.lay_data_extract.takeAt(i).widget().deleteLater()

        # Step 3 : For each axis, adding a WDataExtractor widget inside the layout
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
            wid.refreshNeeded.connect(self.update_needed)

        self.update_needed()

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
        if self.w_axis_2.get_current_axis_selected() != "None":
            axes_selected.append(self.w_axis_2.get_axis_unit_selected())

        return axes_selected

    def get_operation_selected(self):
        """Method that return the actions chosen by the user and the related axis as a string
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
            actions_selected.append(widget.get_operation_selected())

        return actions_selected

    def fft_sync(self):
        """Method that will check the operation chosen and that update the other operation combobox to have the same operation.
        So that, by default, we have FFT and FFT or "" and ""
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object

        """

        operation_selected = self.w_axis_1.get_current_operation_name()
        self.w_axis_2.set_operation(operation_selected)
        self.gen_data_selection()

    def set_axis_widgets(self, data, user_input_list):
        """Method used to set the axes of the Axes group box as well as setting the widgets of the DataSelection groupbox
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            The DataND object that we want to plot
        user_input_list : list
            list of the inputs from the user to set the axes (auto-plot)
        """

        # Step 1 : If user_input are given (auto-plot), we have to process them
        axes_list = list()
        slices_op_list = list()

        for axis in user_input_list:
            if axis.extension in EXTENSION_DICT["axis"]:
                axes_list.append(axis)

            elif axis.extension in EXTENSION_DICT["slice"]:
                slices_op_list.append(axis)

        # Step 2 : Ff we have user input, the we set the UI according to user_input.
        # Otherwise we use the default info
        self.w_axis_1.blockSignals(True)
        self.w_axis_2.blockSignals(True)

        if len(user_input_list) == 0:
            # Case where no user_input was given
            # Sending the info of data to the widget (mainly the axis)
            self.w_axis_1.update(data)
            self.w_axis_2.update(data, axis_name="Y")
            self.axes_list = data.get_axes()

            # Updating w_axis_2 according to w_axis_1 then generating DataSelection
            self.axis_1_updated()

        else:
            # Case where a userinput was given (auto plot)
            # Sending the info of data to the widget (mainly the axis)
            self.w_axis_1.update(data)
            # Setting the axis selected in w_axis_1 according to user_input_list
            self.w_axis_1.set_axis(axes_list[0])
            self.w_axis_2.update(data, axis_name="Y")
            self.axes_list = data.get_axes()

            # Updating w_axis_2 according to w_axis_1 then generating DataSelection
            self.axis_1_updated()

            # Setting the axis selected in w_axis_1 according to user_input_list if we have a second axis
            if len(axes_list) == 2:
                self.w_axis_2.set_axis(axes_list[1])

            # Making sure that we have the same fft/ifft selected for both axis and generating DataSelection again
            self.axis_2_updated()
            self.set_data_selec(slices_op_list)

        self.w_axis_1.blockSignals(False)
        self.w_axis_2.blockSignals(False)

    def set_data_selec(self, user_input_list):
        """Method that set the right operation inside each WDataExtractor inside of w_data_sel
        according to user input (auto plot).
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        user_input_list : list
            list of the inputs from the user to set the DataSelection (auto-plot)
        """
        for wid in self.w_data_sel:
            wid.set_operation(user_input_list[self.w_data_sel.index(wid)])

    def update_needed(self):
        """Method that emits a signal (refreshNeeded) that will be used to automaticaly update the plot inside the GUI.
        This signal is triggered by other signals comming from WDataExtractor or WAxisSelector.
        refreshRange is a different signal that we use to update the values of min and max inside w_range
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """

        self.refreshNeeded.emit()
        self.refreshRange.emit()
