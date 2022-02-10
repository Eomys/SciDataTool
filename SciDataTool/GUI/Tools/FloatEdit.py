# -*- coding: utf-8 -*-
from re import compile, search

from PySide2 import QtGui
from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import QLineEdit

_float_re = compile(r"(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)")


def valid_float_string(string):
    """

    Parameters
    ----------
    string :


    Returns
    -------

    """
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False


class FloatEdit(QLineEdit):
    """A Line Edit Widget optimized to input float"""

    def __init__(self, unit="", *args, **kwargs):
        """Same constructor as QLineEdit + config validator"""

        # Call the Line Edit constructor
        super(FloatEdit, self).__init__(*args, **kwargs)

        # Setup the validator
        Validator = FloatValidator(-1e18, 1e18, 10)
        Validator.Notation = QDoubleValidator.ScientificNotation
        self.setValidator(Validator)

    def focusOutEvent(self, e):
        if self.isModified():
            self.editingFinished.emit()
        self.blockSignals(True)
        super(FloatEdit, self).focusOutEvent(e)
        self.blockSignals(False)

    def keyPressEvent(self, event):
        """To send editingFinished when pressing Enter and Return keys"""
        if event.text() == "\r":
            if self.isModified():
                self.editingFinished.emit()
            self.clearFocus()
        else:
            # call base class keyPressEvent
            QLineEdit.keyPressEvent(self, event)

    def setValue(self, value, is_dB=False):
        """Allow to set the containt of the Widget with a float

        Parameters
        ----------
        self :
            A FloatEdit object
        value :
            A float value to set the Text

        Returns
        -------

        """
        if value is None:
            self.clear()
        else:
            if is_dB:
                self.setText(format(value, ".1f"))
            else:
                self.setText(format(value, ".5g"))

    def value(self):
        """Return the content of the Widget as a float

        Parameters
        ----------
        self :
            A FloatEdit object

        Returns
        -------

        """
        try:
            self.setText(self.validator().fixup_txt(self.text()))
            value = float(self.text())
            return value
        except Exception:
            return None


class FloatValidator(QDoubleValidator):
    """DoubleValidator with fixup method to correct the input"""

    def validate(self, string, position):
        """

        Parameters
        ----------
        string :

        position :


        Returns
        -------

        """
        string = string.replace(",", ".")

        match = search(r"^[+-]?($|(\d+\.?|\.?(\d+|$))\d*($|([eE][+-]?)?\d*$))", string)
        is_intermediate = True if match else False

        if valid_float_string(string):
            state = QtGui.QValidator.Acceptable
        elif is_intermediate:
            state = QtGui.QValidator.Intermediate
        else:
            state = QtGui.QValidator.Invalid
        return (state, string, position)

    def fixup_txt(self, text):
        """When the input text is wrong, fixup is called to correct it in
        the field

        Parameters
        ----------
        self :
            A FloatValidator object
        text :
            The text to correct
        gui_unit :
            Current gui unit system
        val_unit :
            Unit used by the FloatEdit

        Returns
        -------

        """
        if text != "":  # We can't correct an empty text
            # 12,10 can't be converted to float 12.10 can
            text = text.replace(",", ".")
            try:
                top = self.top()
                bottom = self.bottom()

                # If the input is too high...
                if float(text) > top:
                    # ... we replace it by the maximum
                    text = str(top)
                # If the input is too low...
                elif float(text) < bottom:
                    # ... we replace it by the minimum
                    text = str(bottom)
            except ValueError:  # Can't convert value to float => not complete
                pass
        return text
