from PySide2.QtCore import Qt
from PySide2.QtWidgets import QCheckBox


class CheckBox(QCheckBox):
    """To bypass partiallychecked state with user"""

    def __init__(self, *args, **kwargs):
        """Same constructor as QCheckBox"""
        # Call the QCheckBox constructor
        super(CheckBox, self).__init__(*args, **kwargs)
        self.setTristate(True)

    def nextCheckState(self):
        if self.checkState() == Qt.Unchecked:
            super(CheckBox, self).nextCheckState()  # partiallychecked
            super(CheckBox, self).nextCheckState()  # checked
        else:
            super(CheckBox, self).nextCheckState()
