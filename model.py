from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QWidget, QMessageBox

class UsersModel:
    def __init__(self):
        self.model = self.createModel()

    @staticmethod
    def createModel():
        # Táblázatos modell felépítése az SQL tábla alapján
        userTable = QSqlTableModel()
        userTable.setTable("users")
        userTable.setEditStrategy(QSqlTableModel.OnFieldChange)
        userTable.select()
        headers = ("ID", "Név", "Szerepkör", "Email")
        for columnIndex, header in enumerate(headers):
            userTable.setHeaderData(columnIndex, Qt.Horizontal, header)
        return userTable

    def addUser(self, data):
        # Új felhasználó hozzáadása új sor beszúrásával
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def deleteUser(self, index):
        # A megfelelő indexszel rendelkező sor törlése
        self.model.removeRow(index)
        self.model.submitAll()
        self.model.select()

    def clearAll(self):
        # Edit strategy átállítása, hogy az összes rekord egyszerre kezelhetővé váljon
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        # Edit strategy visszaállítása
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

    def searchUser(self, data):
        nev = None
        szk = None
        mail = None
        # Keresett felhasználó adatainak kinyerése
        for i in range(0, self.model.rowCount()):
            record = self.model.record(i)
            if record.value("name") == data:
                nev = record.value("name")
                szk = record.value("role")
                mail = record. value("email")

        box = QWidget()

        if not nev:
            QMessageBox.information(
                box,
                "Hoppá!",
                f"A keresett felhasználó nem létezik!",
                QMessageBox.Ok
            )
        else:
            QMessageBox.information(
                box,
                "Találat",
                f"{nev}\n{szk}\n{mail}",
                QMessageBox.Ok
            )

