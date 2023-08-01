# _*_ coding: utf-8 _*_

"""This module provides view to manage the contacts table."""
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,

)
from PyQt6.QtCore import Qt, QSortFilterProxyModel


from .model import ContactsModel

class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(700, 250)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel=ContactsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's gui."""
        """create table view widget"""
        self.table = QTableView()
        self.proxyModel=QSortFilterProxyModel()
        self.proxyModel.setFilterKeyColumn(-1)
        self.proxyModel.sort(0,Qt.SortOrder.AscendingOrder)

        self.proxyModel.setSourceModel(self.contactsModel.model)
        self.table.setModel(self.proxyModel)
        self.searchbar=QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        self.searchbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.searchbar.setStyleSheet("QLineEdit { border: 2px solid gray;"
                                     "border-radius:10px; }");

        self.searchbar.textChanged.connect(self.proxyModel.setFilterFixedString)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.resizeColumnsToContents()
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearContacts)

        layout = QVBoxLayout()

        layout.addWidget(self.searchbar)
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)

        self.layout.addWidget(self.table,75)
        self.layout.addLayout(layout,25)



    def openAddDialog(self):
        dialog=AddDialog(self)
        if dialog.exec()==QDialog.DialogCode.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteContact(self):
        row=self.table.currentIndex().row()
        if row<0:
            return
        messageBox=QMessageBox.warning(
            self,
            "Warning",
            "Do you want to remove the selected contact?",
            QMessageBox.StandardButton.Ok| QMessageBox.StandardButton.Cancel
        )

        if messageBox==QMessageBox.StandardButton.Ok:
            self.contactsModel.deleteContact(row)

    def clearContacts(self):
        messageBox=QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contacts?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )

        if messageBox==QMessageBox.StandardButton.Ok:
            self.contactsModel.clearContacts()



class AddDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout=QVBoxLayout()
        self.setLayout(self.layout)
        self.data=None
        self.setupUI()

    def setupUI(self):
        self.nameField=QLineEdit()
        self.nameField.setObjectName("Name")
        self.jobField = QLineEdit()
        self.jobField.setObjectName("Job")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        self.descriptionField = QLineEdit()
        self.descriptionField.setObjectName("Description")
        layout=QFormLayout()
        layout.addRow("Name",self.nameField)
        layout.addRow("Job", self.jobField)
        layout.addRow("Email", self.emailField)
        layout.addRow("Description", self.descriptionField)
        self.layout.addLayout(layout)
        buttonsBox=QDialogButtonBox(self)
        buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        buttonsBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttonsBox.accepted.connect(self.accept)
        buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(buttonsBox)

    def accept(self):
        self.data=[]
        for field in (self.nameField,self.jobField, self.emailField, self.descriptionField):
            if not field.text() and field.objectName() != "Job" and field.objectName()!="Description":
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}"
                )

                self.data=None
                return

            self.data.append(field.text())
        super().accept()





