# _*_ coding: utf-8 _*_

"""This module provides model to manage the Contacts table."""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel


class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    def addContact(self,data):
        rows=self.model.rowCount()
        self.model.insertRows(rows,1)
        for column,field in enumerate(data):
            self.model.setData(self.model.index(rows,column+1),field)
        self.model.submitAll()
        self.model.select()
    def deleteContact(self,row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()


    def clearContacts(self):
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.removeRows(0,self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.select()



    @staticmethod
    def _createModel():
        tableModel = QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        tableModel.select()
        headers = ("ID","Name", "Job", "Email", "Description")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel
