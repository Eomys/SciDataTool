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
        # self.c_operation.currentTextChanged.connect(self.update_operation)

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
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            return [key for key in axes_dict][[axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())] 
        else:
            return self.c_axis.currentText() 

        #return self.c_axis.currentText()

    # def get_current_ope_name(self):
    #     """Method that return the operation currently selected
    #     Parameters
    #     ----------
    #     self : WAxisSelector
    #         a WAxisSelector object
    #     Output
    #     ---------
    #     string
    #         name of the current operation selected
    #     """
    #     return self.c_operation.currentText()


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
            for i in range(len(axes_list)):
                if axes_list[i] in axes_dict:
                    self.c_axis.addItem(axes_dict[axes_list[i]])
                else:
                    self.c_axis.addItem(axes_list[i])
            self.c_axis.blockSignals(False)
            
            self.update_axis()

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
            self.axes_list.append(axis.name)



        # At least one axis must be selected => impossible to have none for X axis
        if self.name.lower() != "x" : 
            self.axes_list.insert(0, "None")


        #Step 2 : Replacing the items inside of the ComboBox with the axes recovered
        self.c_axis.clear()
        for i in range(len(self.axes_list)):
            if self.axes_list[i] in axes_dict:
                self.c_axis.addItem(axes_dict[self.axes_list[i]])
            else:
                self.c_axis.addItem(self.axes_list[i])

    # def set_operation(self,operation):
    #     """Method that set the operation of the WAxisSelector 
    #     Parameters
    #     ----------
    #     self : WAxisSelector
    #         a WAxisSelector object
    #     operation : string
    #         name of the new operation"""
        
    #     if operation =="":
    #         self.c_operation.setCurrentIndex(0)

    #     if operation == "FFT":
    #         self.c_operation.setCurrentIndex(1)



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
        self.set_unit()
        print(self.quantity)


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

        #Step 2 : Adding the right units according to a dictionnary
        if self.quantity == "None":
            #If the axis is not selected, then we can not choose the unit
            self.c_unit.clear()
            self.c_unit.setDisabled(True)
        else:
            self.c_unit.setDisabled(False)
            self.c_unit.clear()

            if self.quantity in unit_dict:
                self.c_unit.addItem(unit_dict[self.quantity])



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
        #Updating the units and the quantity selected
        #Making sure that self.quantity is a "tag" and not a "label". Example : z instead of axial direction
        if self.c_axis.currentText() in [axes_dict[key] for key in axes_dict]:
            self.quantity = [key for key in axes_dict][[axes_dict[key] for key in axes_dict].index(self.c_axis.currentText())] 
        else:
            self.quantity = self.c_axis.currentText() 

        #Handling specific case to disable certain parts of the GUI
        if self.c_axis.currentText() == "None":
            self.c_operation.setDisabled(True)
        else:
            self.c_operation.setDisabled(False)

        self.set_unit() 

        #Emitting the signals
        self.refreshNeeded.emit()
        self.axisChanged.emit()

    # def update_operation(self):
    #     """Method called when an operation is changed that will emit a signal as well as updating the units available
    #     Parameters
    #     ----------
    #     self : WAxisSelector
    #         a WAxisSelector object

    #     """
    #     if self.c_operation.currentText() == "Filter":
    #         self.b_filter.setDisabled(False)

    #     else:
    #         self.b_filter.setDisabled(True)
    #         self.refreshNeeded.emit()
    #         self.opeChanged.emit()
