from PySide2.QtWidgets import QSpacerItem, QWidget
from PySide2.QtCore import Signal

from SciDataTool.GUI.WAxisManager.Ui_WAxisManager import Ui_WAxisManager
from SciDataTool.GUI.WSliceOperator.WSliceOperator import WSliceOperator
from SciDataTool.Functions import axes_dict, rev_axes_dict
from SciDataTool.Functions.Plot import ifft_dict, fft_dict


EXTENSION_DICT = {
    "slice": ["max", "min", "rss", "sum", "rms", "mean", "list", "single"],
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
    generateAnimation = Signal()

    def __init__(self, parent=None):
        """Initializing the widget by hiding/showing widget and connecting buttons

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
        self.path_to_image = None

        # Managing the signal emitted by the WAxisSelector widgets
        self.w_axis_1.axisChanged.connect(self.axis_1_updated)
        self.w_axis_2.axisChanged.connect(self.axis_2_updated)

        # The action in axis 2 is by default the one chosen in axis 1
        self.w_axis_1.actionChanged.connect(lambda: self.fft_sync("axis 1"))
        self.w_axis_2.actionChanged.connect(lambda: self.fft_sync("axis 2"))

        self.w_axis_1.refreshNeeded.connect(self.update_needed)
        self.w_axis_2.refreshNeeded.connect(self.update_needed)

    def axis_1_updated(self):
        """Method that remove the axis selected in w_axis_1 from w_axis_2 and call the method that generates
        the layout with the WDataExtractor.
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """
        # Making sure that when axis 1 is updated, axis 1 and 2 are both on "None" for the action combobox
        self.fft_sync("axis 1")

        # Recovering the axis selected by the user removing it from the the second axis combobox
        self.w_axis_2.remove_axis(self.w_axis_1.get_axis_selected())

    def axis_2_updated(self):
        """Method that make sure that when axis 2 is selected (None->?) it has the same fft/ifft combobox selected as axis1
         then generates Data Selection
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """
        # Making sure that when axis 1 is updated, axis 1 and 2 are both on "None" for the action combobox
        self.fft_sync("axis 1")

    def gen_slice_op(self, axes_request_list=None):
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
        axis_selected_1 = self.w_axis_1.get_axis_selected()
        axis_selected_2 = self.w_axis_2.get_axis_selected()

        if axis_selected_1 in axes_list_1:
            axes_list_1.remove(axis_selected_1)
        if axis_selected_2 in axes_list_2:
            axes_list_2.remove(axis_selected_2)

        # Selecting the axes that are in common between the two axes lists
        axes_gen = list()
        axes_gen = [ax for ax in axes_list_1 if ax in axes_list_2]

        for ax in self.axes_list:
            if ax.is_overlay:
                axes_gen.append(ax.name)

        # Step 2 : Removing the items that are in the layout currently
        for i in reversed(range(self.lay_data_extract.count())):
            widget_to_del = self.lay_data_extract.takeAt(i).widget()
            widget_to_del.deleteLater()

        # Step 3 : For each axis available, adding a WSliceOperator widget inside the layout
        # If there are no slice to do (two axis available and selected before) then we hide the groupBox
        if len(axes_gen) != 0:
            self.g_data_extract.show()
            self.w_slice_op = list()

            for axis in axes_gen:
                temp = WSliceOperator(
                    self.g_data_extract, path_to_image=self.path_to_image
                )
                temp.setObjectName(axis)
                for i, ax in enumerate(self.axes_list):
                    if (
                        ax.name == axis
                        or axis in axes_dict
                        and ax.name in axes_dict[axis]
                        or axis in rev_axes_dict
                        and ax.name in rev_axes_dict[axis]
                    ):
                        if axes_request_list is not None and axis in [
                            x.name for x in axes_request_list
                        ]:
                            temp.update(
                                ax,
                                axis_request=axes_request_list[
                                    [x.name for x in axes_request_list].index(axis)
                                ],
                            )
                        else:
                            temp.update(ax)
                temp.refreshNeeded.connect(self.update_needed)
                temp.generateAnimation.connect(self.gen_animate)
                self.w_slice_op.append(temp)
                self.lay_data_extract.addWidget(temp)

        else:
            self.w_slice_op = list()
            self.g_data_extract.hide()
        self.update_needed()

    def gen_animate(self):
        """Methods called after clicking on animate button to generate a gif on the axis selected and display it
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object

        Output
        ---------
        None
        """

        self.generateAnimation.emit()

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
        if self.w_axis_2.get_axis_unit_selected() != "None":
            axes_selected.append(self.w_axis_2.get_axis_unit_selected())

        return axes_selected

    def get_operation_selected(self):
        """Method that return the operations chosen by the user and the related axis as a string
         so that we can use them to plot the data.
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        Output
        ---------
        string
            name of the operation and its axis
        """
        operations_selected = list()

        for wid in self.w_slice_op:
            ope_selected, is_animate = wid.get_operation_selected()

            if is_animate == True:

                axis = ope_selected.split("=")[0]
                unit = "{" + ope_selected.split("{")[1]
                operations_selected.append(axis + "[oneperiod]" + unit + "to_animate")
                wid.is_animate = False
            else:
                operations_selected.append(ope_selected)

        return operations_selected

    def fft_sync(self, axis_changed):
        """Method that will check the action chosen and that update the other action combobox to have the same action.
        So that, by default, we have FFT and FFT or "None" and "None"
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object

        """
        if axis_changed == "axis 1" and "FFT" in [
            self.w_axis_1.c_action.itemText(i)
            for i in range(self.w_axis_1.c_action.count())
        ]:
            action_selected = self.w_axis_1.get_current_action_name()
            self.w_axis_2.set_action(action_selected)
            if action_selected == "FFT":
                if self.w_axis_2.axis_selected in fft_dict:
                    if self.w_axis_2.axis_selected in self.w_axis_2.axes_list:
                        self.w_axis_2.axes_list[
                            self.w_axis_2.axes_list.index(self.w_axis_2.axis_selected)
                        ] = fft_dict[self.w_axis_2.axis_selected]
                        self.w_axis_2.axis_selected = fft_dict[
                            self.w_axis_2.axis_selected
                        ]
                    else:
                        self.w_axis_2.axis_selected = fft_dict[
                            self.w_axis_2.axis_selected
                        ]
                elif self.w_axis_2.axis_selected in ifft_dict:
                    if (
                        self.w_axis_2.axis_selected not in self.w_axis_2.axes_list
                        and ifft_dict[self.w_axis_2.axis_selected]
                        in self.w_axis_2.axes_list
                    ):
                        self.w_axis_2.axes_list[
                            self.w_axis_2.axes_list.index(
                                ifft_dict[self.w_axis_2.axis_selected]
                            )
                        ] = self.w_axis_2.axis_selected
            else:
                if self.w_axis_2.axis_selected in ifft_dict:
                    if self.w_axis_2.axis_selected in self.w_axis_2.axes_list:
                        self.w_axis_2.axes_list[
                            self.w_axis_2.axes_list.index(self.w_axis_2.axis_selected)
                        ] = ifft_dict[self.w_axis_2.axis_selected]
                        self.w_axis_2.axis_selected = ifft_dict[
                            self.w_axis_2.axis_selected
                        ]
                    else:
                        self.w_axis_2.axis_selected = ifft_dict[
                            self.w_axis_2.axis_selected
                        ]
                elif self.w_axis_2.axis_selected in fft_dict:
                    if (
                        self.w_axis_2.axis_selected not in self.w_axis_2.axes_list
                        and fft_dict[self.w_axis_2.axis_selected]
                        in self.w_axis_2.axes_list
                    ):
                        self.w_axis_2.axes_list[
                            self.w_axis_2.axes_list.index(
                                fft_dict[self.w_axis_2.axis_selected]
                            )
                        ] = self.w_axis_2.axis_selected
            self.gen_slice_op()
            self.w_axis_2.set_unit()

        elif axis_changed == "axis 2" and "FFT" in [
            self.w_axis_2.c_action.itemText(i)
            for i in range(self.w_axis_2.c_action.count())
        ]:
            action_selected = self.w_axis_2.get_current_action_name()
            self.w_axis_1.set_action(action_selected)
            if action_selected == "FFT":
                if self.w_axis_1.axis_selected in fft_dict:
                    if self.w_axis_1.axis_selected in self.w_axis_1.axes_list:
                        self.w_axis_1.axes_list[
                            self.w_axis_1.axes_list.index(self.w_axis_1.axis_selected)
                        ] = fft_dict[self.w_axis_1.axis_selected]
                        self.w_axis_1.axis_selected = fft_dict[
                            self.w_axis_1.axis_selected
                        ]
                    else:
                        self.w_axis_1.axis_selected = fft_dict[
                            self.w_axis_1.axis_selected
                        ]
                elif self.w_axis_1.axis_selected in ifft_dict:
                    if (
                        self.w_axis_1.axis_selected not in self.w_axis_1.axes_list
                        and ifft_dict[self.w_axis_1.axis_selected]
                        in self.w_axis_1.axes_list
                    ):
                        self.w_axis_1.axes_list[
                            self.w_axis_1.axes_list.index(
                                ifft_dict[self.w_axis_1.axis_selected]
                            )
                        ] = self.w_axis_1.axis_selected
            else:
                if self.w_axis_1.axis_selected in ifft_dict:
                    if self.w_axis_1.axis_selected in self.w_axis_1.axes_list:
                        self.w_axis_1.axes_list[
                            self.w_axis_1.axes_list.index(self.w_axis_1.axis_selected)
                        ] = ifft_dict[self.w_axis_1.axis_selected]
                        self.w_axis_1.axis_selected = ifft_dict[
                            self.w_axis_1.axis_selected
                        ]
                    else:
                        self.w_axis_1.axis_selected = ifft_dict[
                            self.w_axis_1.axis_selected
                        ]
                elif self.w_axis_1.axis_selected in fft_dict:
                    if (
                        self.w_axis_1.axis_selected not in self.w_axis_1.axes_list
                        and fft_dict[self.w_axis_1.axis_selected]
                        in self.w_axis_1.axes_list
                    ):
                        self.w_axis_1.axes_list[
                            self.w_axis_1.axes_list.index(
                                fft_dict[self.w_axis_1.axis_selected]
                            )
                        ] = self.w_axis_1.axis_selected
            self.gen_slice_op()
            self.w_axis_1.set_unit()

    def set_axis_widgets(
        self,
        data,
        axes_request_list,
        frozen_type=0,
        is_keep_config=False,
        path_to_image=None,
    ):
        """Method used to set the axes of the Axes group box as well as setting the widgets of the DataSelection groupbox
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            The DataND object that we want to plot
        axes_request_list:
            list of RequestedAxis which are the info given for the autoplot (for the axes and DataSelection)
        frozen_type : int
            0 to let the user modify the axis of the plot, 1 to let him switch them, 2 to not let him change them, 3 to freeze both axes and operations, 4 to freeze fft
        path_to_image : str
            path to the folder where the image for the animation button is saved
        """
        # Setting path to recover the image for the animate button
        self.path_to_image = path_to_image
        self.w_axis_1.path_to_image = self.path_to_image
        self.w_axis_2.path_to_image = self.path_to_image

        if is_keep_config:  # Only update slider
            for wid in self.w_slice_op:
                if hasattr(wid, "axis_value"):
                    wid.update_floatEdit()
            axes_list = data.get_axes()

        else:
            # Step 1 : If only one axis is given with the object, then we hide w_axis_2 and g_data_extract
            # We also have to hide if we have more than one axis but one have is_overlay = True
            if len(data.get_axes()) == 1 or (
                len(data.get_axes())
                - len([ax for ax in data.get_axes() if ax.is_overlay == True])
                == 1
            ):
                self.w_axis_2.hide()
                self.g_data_extract.hide()

            else:
                self.w_axis_2.show()
                self.g_data_extract.show()

            # Step 2 : If we have user input, the we set the UI according to user_input.
            # Otherwise we use the default info
            self.w_axis_1.blockSignals(True)
            self.w_axis_2.blockSignals(True)

            # Reinitialize filter indices
            self.w_axis_1.indices = None
            self.w_axis_2.indices = None

            if axes_request_list == []:
                # Case where no user_input was given
                # Sending the info of data to the widget (mainly the axis)
                self.axes_list = data.get_axes()
                self.w_axis_1.update(self.axes_list)
                self.w_axis_2.update(self.axes_list, axis_name="Y")

                # Updating w_axis_2 according to w_axis_1 then generating DataSelection
                self.axis_1_updated()
                axes_list = self.axes_list

            else:
                # Case where a userinput was given (auto plot)

                # If user_input are given (auto-plot), we have to process them
                axes_list = [
                    ax
                    for ax in axes_request_list
                    if ax.extension in EXTENSION_DICT["axis"]
                ]

                slices_op_list = [
                    ax
                    for ax in axes_request_list
                    if ax.extension in EXTENSION_DICT["slice"]
                ]

                # Sending the info of data to the widget (mainly the axis)
                self.axes_list = data.get_axes()
                self.w_axis_1.update(self.axes_list)
                self.w_axis_2.update(self.axes_list, axis_name="Y")
                # Setting the axis selected in w_axis_1 according to user_input_list
                self.w_axis_1.set_axis(axes_list[0])

                # Updating w_axis_2 according to w_axis_1 then generating DataSelection
                self.axis_1_updated()

                # Setting the axis selected in w_axis_1 according to user_input_list if we have a second axis
                if len(axes_list) == 2:
                    self.w_axis_2.set_axis(axes_list[1])

                # Making sure that we have the same fft/ifft selected for both axis
                self.axis_2_updated()

                # Generating DataSelection with the input of user if they are given or by default (like in a manual plot)
                if len(slices_op_list) != 0:
                    self.gen_slice_op(axes_request_list)
                    self.set_slice_op(slices_op_list)
                else:
                    self.gen_slice_op(axes_request_list)

        # Depending on the value of frozen type we are going to act on the UI
        if frozen_type == 1 and len(axes_list) == 2:
            # Recovering the axis requested by the user as they will be soft frozen (possible to switch but not possible to choose another axis)
            axes_list_name = [ax.name for ax in axes_list]
            axes_soft_frozen = [
                ax for ax in self.axes_list if ax.name in axes_list_name
            ]

            # We update the WAxisSelector widget with the axes that will be soft frozen
            self.w_axis_1.update(axes_soft_frozen)
            self.w_axis_2.update(axes_soft_frozen)

            self.axis_1_updated()

        elif frozen_type == 2:
            # If we want to hard freeze the axis, we just have to disable the axis comboboxes
            self.w_axis_1.c_axis.setDisabled(True)
            self.w_axis_2.c_axis.setDisabled(True)

        elif frozen_type == 3:
            # Freezing the axes
            self.w_axis_1.c_axis.setDisabled(True)
            self.w_axis_1.c_action.setDisabled(True)
            self.w_axis_2.c_axis.setDisabled(True)
            self.w_axis_2.c_action.setDisabled(True)

            # Freezing the operations
            for w_slice in self.w_slice_op:
                w_slice.b_action.setDisabled(True)
                w_slice.c_operation.setDisabled(True)
                w_slice.lf_value.setDisabled(True)
                w_slice.slider.setDisabled(True)

        elif frozen_type == 4:
            self.w_axis_1.c_axis.setDisabled(True)
            self.w_axis_2.c_axis.setDisabled(True)
            if axes_list[0].name in ifft_dict or axes_list[0].name in fft_dict:
                self.w_axis_1.c_action.setDisabled(True)
            if len(axes_list) == 2 and (
                axes_list[1].name in ifft_dict or axes_list[0].name in fft_dict
            ):
                self.w_axis_2.c_action.setDisabled(True)

        if len(axes_list) == 1:
            self.w_axis_2.hide()

        self.w_axis_1.blockSignals(False)
        self.w_axis_2.blockSignals(False)

    def set_slice_op(self, user_input_list):
        """Method that set the right operation inside each WSliceOperator inside of w_slice_op
        according to user input (auto plot).
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        user_input_list : list
            list of the inputs from the user to set the DataSelection (auto-plot)
        """
        for wid in self.w_slice_op:
            if self.w_slice_op.index(wid) < len(user_input_list):
                wid.set_operation(user_input_list[self.w_slice_op.index(wid)])

    def update_needed(self):
        """Method that emits a signal (refreshNeeded) that will be used to automaticaly update the plot inside the GUI.
        This signal is triggered by other signals comming from WSliceOperator or WAxisSelector.
        refreshRange is a different signal that we use to update the values of min and max inside w_range
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        """

        self.refreshNeeded.emit()
        self.refreshRange.emit()
