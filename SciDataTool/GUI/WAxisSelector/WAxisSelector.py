from PySide2.QtWidgets import QWidget

from ...GUI.WAxisSelector.Ui_WAxisSelector import Ui_WAxisSelector
from PySide2.QtCore import Signal
from ...Functions.Plot import unit_dict,axes_dict


class WAxisSelector(Ui_WAxisSelector, QWidget):
    """Widget to select the axis to plot"""

    refreshNeeded = Signal()
    axisChanged = Signal()
    opeChanged = Signal()

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

        self.name = "X"         #Name of the axis
        self.axes_list = list() #List of the different axes of the DataND object
        self.quantity = ""      #Name of the quantity of the axis (for ex: time, angle...)

        self.b_filter.setDisabled(True)

        self.c_axis.currentTextChanged.connect(self.update_axis)
        self.c_operation.currentTextChanged.connect(self.update_operation)

    def change_name(self,axis_name):
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
        return self.c_axis.currentText()

    def get_current_ope_name(self):
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

    def remove_axis(self,axis_to_remove):
        """Method that remove a given axis from the axis ComboBox.
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis_to_remove : string
            name of the axis to remove from c_axis

        """
        if axis_to_remove in self.axes_list:
            axes_list = self.axes_list[:]       #Getting the axes available
            axes_list.remove(axis_to_remove)    #Removing the axis seleted

            #Building the new ComboBox
            self.c_axis.blockSignals(True)
            self.c_axis.clear()
            self.c_axis.addItems(axes_list)
            self.c_axis.blockSignals(False)

    def set_axis(self,data):
        """Method that will put the axes of data in the combobox of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        data : DataND
            A DataND object that we want to plot

        """
        
        #Step 1 : Getting the name of the different axes of the DataND object
        for axis in data.get_axes():
            if any(axis.name in key for key in axes_dict):
                self.axes_list.append(axes_dict[axis.name])

            else:
                self.axes_list.append(axis.name)

        # At least one axis must be selected => impossible to have none for X axis
        if self.name.lower() != "x" : 
            self.axes_list.insert(0, "None")


        #Step 2 : Replacing the items inside of the ComboBox with the axes recovered
        self.c_axis.clear()
        self.c_axis.addItems(self.axes_list)

    def set_quantity(self,new_quantity):
        """Method that set the quantity of the WAxisSelector 
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        new_quantity : string
            name of the new quantity

        """
        self.quantity = new_quantity
        self.set_unit(self.quantity)


    def set_unit(self,axis = ""):
        """Method that update the unit comboxbox according to the axis selected in the other combobox.
           We can also give the axis selected and put its units inside the combobox
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis : string
            name of the axis that is selected
        """

        if axis == "":
            #Step 1 : Recovering the axis chosen 
            quantity = self.c_axis.currentText()

            #Step 2 : Adding the right units according to a dictionnary
            if quantity == "None":
                #If the axis is not selected, then we can not choose the unit
                self.c_unit.clear()
                self.c_unit.setDisabled(True)
            else:
                self.c_unit.setDisabled(False)
                self.c_unit.clear()

                if quantity in unit_dict:
                    self.c_unit.addItem(unit_dict[quantity])

        else:
            self.c_unit.clear()
            self.c_unit.addItem(unit_dict[axis])

    def update(self,data,axis_name = "X"):
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
             
    def update_axis(self):
        """Method called when an axis is changed that will emit a signal as well as updating the units available
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        #Updating the units and the quantity seleted
        self.set_unit()  
        self.quantity = self.c_axis.currentText() 

        #Handling specific case to disable certain parts of the GUI
        if self.c_axis.currentText() == "None":
            self.c_operation.setDisabled(True)
        else:
            self.c_operation.setDisabled(False)

        self.refreshNeeded.emit()
        self.axisChanged.emit()

    def update_operation(self):
        """Method called when an operation is changed that will emit a signal as well as updating the units available
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        if self.c_operation.currentText() == "Filter":
            self.b_filter.setDisabled(False)
        
        else:
            self.b_filter.setDisabled(True)
            self.refreshNeeded.emit()
            self.opeChanged.emit()
