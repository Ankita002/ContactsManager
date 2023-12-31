# _*_ coding: utf-8 _*_

"""This module provides a database connection."""

from PyQt6.QtWidgets import QMessageBox

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable():
    createTableQuery=QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            job VARCHAR(50),
            email VARCHAR(40) NOT NULL,
            description VARCHAR(100)
        )
        """
    )

def createConnection(databaseName):
    connection=QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(None,
                            "Contact",
                            f"Database Error: {connection.lastError().text()}"
                            )
        return False
    _createContactsTable()
    return True
