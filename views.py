from model import UsersModel
import pandas as pd
import xlsxwriter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox
)

class Window(QMainWindow):
    # Alkalmazás főablaka
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Felhasználók")
        self.resize(800, 500)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.userModel = UsersModel()
        self.setupUI()

    def openAddDialog(self):
        # Új felhasználó párbeszéd ablak megnyitása
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.userModel.addUser(dialog.data)
            self.table.resizeColumnsToContents()

    def openSearchDialog(self):
        # Felhasználó keresés párbeszéd ablak megnyitása
        dialog = SearchDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.userModel.searchUser(dialog.data)

    def deleteUser(self):
        # Kiválasztott rekord törlése
        index = self.table.currentIndex().row()
        if index < 0:
            return
        msgbox = QMessageBox.warning(
            self,
            "Biztos?",
            "Törölni szeretnéd a kiválasztott felhasználót?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if msgbox == QMessageBox.Ok:
            self.userModel.deleteUser(index)

    def clearAll(self):
        # Összes rekord törlése
        msgbox = QMessageBox.warning(
            self,
            "Biztos?",
            "Törölni szeretnéd az összes felhasználót?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if msgbox == QMessageBox.Ok:
            self.userModel.clearAll()

    def save(self):
        # Mentés Excel fájlba
        listofNames = []
        listofRoles = []
        listofEmails = []
        def iterate(list, field):
            for i in range(0, self.userModel.model.rowCount()):
                record = self.userModel.model.record(i)
                list.append(record.value(field))
        iterate(listofNames, "name")
        iterate(listofRoles, "role")
        iterate(listofEmails, "email")

        data = {'Név': listofNames,
                'Szerepkör': listofRoles,
                'Email': listofEmails
                }

        df = pd.DataFrame(data, columns=['Név', 'Szerepkör', 'Email'])
        df.index = range(1, len(df) + 1)
        xlsxwriter.Workbook('users.xlsx')
        df.to_excel(excel_writer='users.xlsx', sheet_name='Felhasználók')
        QMessageBox.information(
            self,
            "Mentés",
            "Sikeres mentés!"
        )


    def setupUI(self):
        # Felhasználói felület a főablakhoz
        # Táblázat létrehozása az adatbázis táblából, majd összekapcsolás az adatmodellel
        self.table = QTableView()
        self.table.setModel(self.userModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        # Gombok létrehozása
        self.addButton = QPushButton("Új kontakt")
        self.addButton.setStyleSheet('background-color: #71797E; color: white;')
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Törlés")
        self.deleteButton.setStyleSheet('background-color: #71797E; color: white;')
        self.deleteButton.clicked.connect(self.deleteUser)
        self.searchButton = QPushButton("Keresés")
        self.searchButton.setStyleSheet('background-color: #71797E; color: white;')
        self.searchButton.clicked.connect(self.openSearchDialog)
        self.saveButton = QPushButton("Mentés")
        self.saveButton.setStyleSheet('background-color: #71797E; color: white;')
        self.saveButton.clicked.connect(self.save)
        self.clearAllButton = QPushButton("Összes törlése")
        self.clearAllButton.setStyleSheet('background-color: #71797E; color: white;')
        self.clearAllButton.clicked.connect(self.clearAll)
        # Gombok és táblázat megjelenítése
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.searchButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.clearAllButton)
        buttonLayout.addStretch()
        self.layout.addWidget(self.table)
        self.layout.addLayout(buttonLayout)


class AddDialog(QDialog):
    # Párbeszéd ablak új felhasználó hozzáadásához
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Új felhasználó")
        self.resize(250, 150)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        # GUI a párbeszéd ablakhoz
        # Beviteli mezők definiálása
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Név")
        self.roleField = QLineEdit()
        self.roleField.setObjectName("Szerepkör")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        # Beviteli mezők megjelenítése
        layout = QFormLayout()
        layout.addRow("Név:", self.nameField)
        layout.addRow("Szerepkör:", self.roleField)
        layout.addRow("Email:", self.emailField)
        self.layout.addLayout(layout)
        # 'Ok' és 'Vissza' gombok definiálása/megjelenítése
        self.buttonsBox = QDialogButtonBox(self)
        self.layout.addWidget(self.buttonsBox)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        # Kattintáskor a megfelelő események triggerelése
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)

    def accept(self):
        # Adatok elfogadása az interakció után
        self.data = []
        # Adatok betöltése a 'data' listába for ciklussal
        for field in (self.nameField, self.roleField, self.emailField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Hiba!",
                    "Minden mezőt ki kell töltened!",
                )
                self.data = None
                return

            self.data.append(field.text())
        if not self.data:
            return
        super().accept()

class SearchDialog(QDialog):
    # Párbeszéd ablak felhasználó kereséséhez
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Keresés")
        self.resize(250, 50)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        # GUI...
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Név")
        layout = QFormLayout()
        layout.addRow("Név:", self.nameField)
        self.layout.addLayout(layout)
        # Gombok...
        self.buttonsBox = QDialogButtonBox(self)
        self.layout.addWidget(self.buttonsBox)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)

    def accept(self):
        # Adatok elfogadása...
        self.data = None
        if not self.nameField.text():
            QMessageBox.critical(
                self,
                "Hiba!",
                f"Meg kell adnod egy nevet!",
            )
            return

        self.data = self.nameField.text()
        if not self.data:
            return
        super().accept()