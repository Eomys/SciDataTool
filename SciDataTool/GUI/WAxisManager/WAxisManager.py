from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QSpacerItem, QWidget

from ...GUI.WAxisManager.Ui_WAxisManager import Ui_WAxisManager
from ...GUI.WAxisSelector.WAxisSelector import AXES_DICT
from ...GUI.WDataExtractor.WDataExtractor import WDataExtractor


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
        self.gen_data_selec(data)

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

            axes_to_show = list ()
            for ax in self.w_axis_1.get_axes():
                if not ax in axes_selected:
                    axes_to_show.append(ax)

            #Step 4 : showing the right axes inside the DataSelection groupBox
            self.show_data_selec(axes_to_show)

    def gen_data_selec(self,data):
        """Method that generates the Data Selection groupbox by adding WdataExtractor Widget to its layout
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            the DataND object that we want to plot
        
        """
        #Step 1 : Getting the name of the different axes of the DataND object
        axes_list = [AXES_DICT[axis.name] 
        for axis in data.get_axes() 
        if axis.name != "phase" and axis.get_length() > 1
        ]

        if "time" in axes_list:
            axes_list.append("frequency")
        elif "frequency" in axes_list:
            axes_list.append("time")
        if "angle" in axes_list:
            axes_list.append("wavenumber")
        elif "wavenumber" in axes_list:
            axes_list.append("angle")            

        #Step 2 Adding a WDataExtractor widget for each axis inside the layout and hiding it
        for axis in axes_list:
            self.w_data_sel = WDataExtractor(self.layoutWidget)
            self.w_data_sel.setObjectName(axis)
            self.w_data_sel.setMinimumSize(QSize(0, 80))
            self.w_data_sel.setMaximumSize(QSize(280, 80))

            self.lay_data_extract.addWidget(self.w_data_sel)

            self.w_data_sel.update(axis)
            self.w_data_sel.hide()

        #Step 3 : Adding a spacer to imrove the UI visually 
        self.verticalSpacer = QSpacerItem(296, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lay_data_extract.addItem(self.verticalSpacer)
        
    def show_data_selec(self,axes_list):
        """Method that show the right WDataExtrator widget according to axes_list and add a
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : axes_list
            list of the axes that should be shown inside DataSelection
        """
        for i in range(self.lay_data_extract.count()-1):
            if self.lay_data_extract.itemAt(i).widget().objectName() in axes_list:
                self.lay_data_extract.itemAt(i).widget().show()
            else:
                self.lay_data_extract.itemAt(i).widget().hide()



