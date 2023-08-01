# _*_ coding: utf-8 _*_

"""This module provides Contacts application."""

import sys

from PyQt6.QtWidgets import QApplication

from .database import createConnection
from .views import Window


def main():
    """Contacts main function."""
    app = QApplication(sys.argv)
    if not createConnection("contacts.sqlite"):
        sys.exit(1)
    win = Window()
    win.show()
    sys.exit(app.exec())
