from PySide2.QtWidgets import QWidget

from ...GUI.WAxisManager.Ui_WAxisManager import Ui_WAxisManager
from ...GUI.WAxisSelector.WAxisSelector import AXES_DICT


class WAxisManager(Ui_WAxisManager, QWidget):
    """Widget that will handle the selection of the axis as well as generating WDataExtractor"""

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

        self.w_axis_1.axisChanged.connect(self.update_axes)
        self.w_axis_2.axisChanged.connect(self.update_axes)


    def set_axes(self,data):
        """Method used to set the axes of the Axes group box (e.g setting up the comboboxes + labels)
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            The DataND object that we want to plot
        """
        self.w_axis_1.update(data)
        self.w_axis_2.update(data,"Y")

    def update_axes(self):
        """Method that will check if the axes chosen are correct and if true it will update the comboboxes
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            the DataND object that we want to plot
        
        """
        #Step 1 : Recovering the axis selected by the user that should not be in data selection
        axes_selected = list()
        axes_selected.append(self.w_axis_1.get_current_axis())
        axes_selected.append(self.w_axis_2.get_current_axis())

        #Step 2 : Handling the case where the selected axes are not correct
        if axes_selected[0] == axes_selected[1]:
            print("Error : Same axis selected for X and Y")

        elif "time" in axes_selected and "frequency" in axes_selected:
            print("Error : You can not select time and frequency as axes at the same time")
        elif "angle" in axes_selected and "wavenumber" in axes_selected:
            print("Error : You can not select angle and wavenumber as axes at the same time")
                
        else:

            #Step 3 : Getting the list of items to generate
            if "time" in axes_selected:
                axes_selected.append("frequency")
            elif "frequency" in axes_selected:
                axes_selected.append("time")
            if "angle" in axes_selected:
                axes_selected.append("wavenumber")
            elif "wavenumber" in axes_selected:
                axes_selected.append("angle")            

            axes_to_gen = list ()
            for ax in self.w_axis_1.get_axes():
                if not ax in axes_selected:
                    axes_to_gen.append(ax)


            print(axes_to_gen)
