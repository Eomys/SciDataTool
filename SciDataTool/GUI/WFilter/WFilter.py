from PySide2.QtWidgets import (
    QWidget,
    QCheckBox,
    QLabel,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
    QApplication,
)
from PySide2.QtCore import Qt, QEvent, QPoint, QRect
from PySide2.QtGui import QStandardItemModel, QStandardItem

from SciDataTool.GUI.WFilter.Ui_WFilter import Ui_WFilter
from PySide2.QtCore import Signal, QSortFilterProxyModel
from SciDataTool.Functions.Plot import axes_dict

# Column id
VALUE_COL = 0
PLOT_COL = 1


class WFilter(Ui_WFilter, QWidget):
    """Widget to select the Data/output range"""

    refreshNeeded = Signal()

    def __init__(self, axis, parent=None):
        """Linking the button with their method + initializing the arguments used

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        parent : QWidget
            The parent QWidget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.axis = axis
        self.axis_values = self.axis.get_values()
        self.init_table()
        tableModel = self.tab_indices.model()
        proxyModel = QSortFilterProxyModel()
        proxyModel.setSourceModel(tableModel)
        self.tab_indices.setModel(proxyModel)

        if self.axis.name in axes_dict:
            self.setWindowTitle("Filtering on " + axes_dict[self.axis.name])
        else:
            self.setWindowTitle("Filtering on " + self.axis.name)

        self.b_Ok.clicked.connect(self.update_and_close)
        self.b_cancel.clicked.connect(self.cancel_and_close)

    def cancel_and_close(self):
        """Method called when the user click on the cancel button
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        self.close()

    def init_table(self):
        """Method that fill the table with the values of the axis, each line corresponds to one index
        Parameters
        ----------
        self : WDataRange
            a WDataRange object"""
        self.tab_indices.setSortingEnabled(True)

        if self.axis.is_components:
            # If we have an axis with components, then we use the filters to build the complete table
            filter_list = list(self.axis.filter.keys())
            filter_list.append("Plot ?")  # Adding the column with checkbox

            # Setting up the table
            data_model = MyTableModel(
                [
                    [string for string in value.split(self.axis.delimiter)]
                    for value in self.axis_values
                ],
                filter_list,
                self,
            )
            for i in range(len(self.axis_values)):
                item = QStandardItem()
                data_model.setItem(i, len(filter_list), item)
            self.tab_indices.setModel(data_model)

            self.tab_indices.setItemDelegateForColumn(
                len(filter_list) - 1, CheckBoxDelegate(self)
            )

        else:
            # Setting up the table
            data_model = MyTableModel(
                [self.axis_values],
                ["Value", "Plot ?"],
                self,
            )
            for i in range(len(self.axis_values)):
                item = QStandardItem()
                data_model.setItem(i, 2, item)
            self.tab_indices.setModel(data_model)

            self.tab_indices.setItemDelegateForColumn(1, CheckBoxDelegate(self))

    def update_and_close(self):
        """Method called when the click on the Ok button
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        self.close()


class MyTableModel(QStandardItemModel):
    def __init__(self, datain, header, parent=None):
        QStandardItemModel.__init__(self, parent)
        self.arraydata = datain
        self.header_labels = header

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.header_labels)

    def data(self, index, role):
        if role == Qt.EditRole:
            print("edit mode")
            return None
        elif role != Qt.DisplayRole:
            return None
        if index.column() == self.columnCount(None) - 1:
            return self.itemFromIndex(index)
        else:
            return self.arraydata[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QStandardItemModel.headerData(self, section, orientation, role)


class CheckBoxDelegate(QStyledItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every
    cell of the column to which it's applied
    """

    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        ** Need to hook up a signal to the model
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """

        checked = index.data().checkState().__bool__()
        check_box_style_option = QStyleOptionButton()

        if (index.flags() & Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QStyle.State_Enabled
        else:
            check_box_style_option.state |= QStyle.State_ReadOnly

        if checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)

        check_box_style_option.state |= QStyle.State_Enabled

        QApplication.style().drawControl(
            QStyle.CE_CheckBox, check_box_style_option, painter
        )

    def editorEvent(self, event, model, option, index):
        """
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        """
        if not (index.flags() & Qt.ItemIsEditable) > 0:
            return False

        # Do not change the checkbox-state
        if event.type() == QEvent.MouseButtonPress:
            return False
        if (
            event.type() == QEvent.MouseButtonRelease
            or event.type() == QEvent.MouseButtonDblClick
        ):
            if event.button() != Qt.LeftButton or not self.getCheckBoxRect(
                option
            ).contains(event.pos()):
                return False
            if event.type() == QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.KeyPress:
            if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                return False
        else:
            return False

        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData(self, editor, model, index):
        """
        The user wanted to change the old state in the opposite.
        """
        newValue = not index.data().checkState().__bool__()
        model.setData(index, newValue, Qt.EditRole)

    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(
            QStyle.SE_CheckBoxIndicator, check_box_style_option, None
        )
        check_box_point = QPoint(
            option.rect.x() + option.rect.width() / 2 - check_box_rect.width() / 2,
            option.rect.y() + option.rect.height() / 2 - check_box_rect.height() / 2,
        )
        return QRect(check_box_point, check_box_rect.size())