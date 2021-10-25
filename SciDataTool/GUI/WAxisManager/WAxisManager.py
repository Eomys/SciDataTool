from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QSpacerItem, QWidget

from ...GUI.WAxisManager.Ui_WAxisManager import Ui_WAxisManager
from ...GUI.WDataExtractor.WDataExtractor import WDataExtractor

LINKED_AXIS ={
    "time":["time","frequency"],
    "frequency":["time","frequency"],
    "angle":["angle","wavenumber"],
    "wavenumber":["angle","wavenumber"],
    "None" : [],
    "axial direction": [],
}

COMP_AXIS = {
    "time":["angle","axial direction"],
    "angle":["time","axial direction"],
    "frequency":["wavenumber"],
    "wavenumber":["frequency"],
    "axial direction":["time","angle"],
}

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

        self.w_axis_1.axisChanged.connect(self.axes_updated)
        self.w_axis_2.axisChanged.connect(self.axes_updated)

    def set_axes(self,data):
        """Method used to set the axes of the Axes group box as well as setting the widgets of the DataSelection groupbox
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            The DataND object that we want to plot
        """

        self.w_axis_1.update(data)
        self.w_axis_2.update(data,"Y")



    def axes_updated(self):
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
        axes_selected.append(self.w_axis_1.get_current_axis_name())
        axes_selected.append(self.w_axis_2.get_current_axis_name())

        #Step 2 : Handling the case where the selected axes are not correct
        if axes_selected[1] in LINKED_AXIS[axes_selected[0]] or axes_selected[0] in LINKED_AXIS[axes_selected[1]]:
            print("Error : Wrong axes combination selected")
 
        else:
   
            #Step 3 : Adding the FFT/IFFT of the axis given
            axes_selected += [axis for axis in LINKED_AXIS[axes_selected[0]] if axis != axes_selected[0]]
            axes_selected += [axis for axis in LINKED_AXIS[axes_selected[1]] if axis != axes_selected[1]]
                    
            axes_to_gen = list()
            for ax in self.w_axis_1.get_axes(): #TO MODIFY
                if not ax in axes_selected:
                    axes_to_gen.append(ax)
            #Step 4 : showing the right axes inside the DataSelection groupBox
            self.gen_data_selec(axes_to_gen)


        
    def gen_data_selec(self,axes_list):
        """Method that gen the right WDataExtrator widget according to axes_list 
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : axes_list
            list of the axes that should be shown inside DataSelection
        """
        #Step 1 : Deleting items in the layout currently
        if isinstance(self.lay_data_extract.takeAt(self.lay_data_extract.count()-1),QSpacerItem):
            self.lay_data_extract.takeAt(self.lay_data_extract.count()-1).widget().deleteLater()        #if isinstance(self.lay_data_extract.takeAt(self.lay_data_extract.count()-1),QSpacerItem):

        for i in reversed(range (self.lay_data_extract.count())):
            test = self.lay_data_extract.takeAt(i).widget()
            test.deleteLater()

            
        #Step 2 : Adding a WDataExtractor widget for each axis inside the layout 
        for axis in axes_list:
            self.w_data_sel = WDataExtractor(self.layoutWidget)
            self.w_data_sel.setObjectName(axis)
            self.w_data_sel.setMinimumSize(QSize(0, 80))
            self.w_data_sel.setMaximumSize(QSize(280, 80))

            self.lay_data_extract.addWidget(self.w_data_sel)

            self.w_data_sel.update(axis)

        #Step 3 : Adding a spacer to improve the UI visually 
        self.verticalSpacer = QSpacerItem(296, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lay_data_extract.addItem(self.verticalSpacer)




