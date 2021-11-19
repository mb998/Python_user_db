import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from database import createConnection
from views import Window

def main():
    # Az applikációt létrehozó függvény
    app = QApplication(sys.argv)
    msgWidget = QWidget()
    # Kapcsolat hiánya esetén hibaüzenet
    if not createConnection("users.db"):
        QMessageBox.warning(
            msgWidget,
            "Nincs kapcsolat",
            "Nem lehetett kapcsolódni az adatbázishoz!",
            QMessageBox.Ok,
        )
        sys.exit(1)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec())