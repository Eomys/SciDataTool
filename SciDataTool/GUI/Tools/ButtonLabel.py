from PySide2.QtWidgets import QLabel


class ButtonLabel(QLabel):
    """A QLabel Widget for buttons with hovering stylesheet"""

    def __init__(self, *args, **kwargs):
        """Same constructor as QLabel"""

        # Call the QLabel constructor
        super(ButtonLabel, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setStyleSheet(
            ".ButtonLabel{border: 1px solid transparent; border-radius: 6px;}"
        )

    def enterEvent(self, event):
        """To add border when hovering label"""
        self.setStyleSheet(
            ".ButtonLabel{border: 1px solid #0069A1; border-radius: 6px;}"
        )

    def leaveEvent(self, event):
        """To remove border when leaving label"""
        self.setStyleSheet(
            ".ButtonLabel{border: 1px solid transparent; border-radius: 6px;}"
        )
