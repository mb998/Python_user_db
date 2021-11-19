from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def createUserTable():
    # Users adatbázis tábla létrehozása SQL query segítségével
    createUsersTable = QSqlQuery()
    return createUsersTable.exec(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            role VARCHAR(50),
            email VARCHAR(40) NOT NULL
        )
        """
    )


def createConnection(dbName):
    # Kapcsolat létrehozása az SQLite adatbázissal
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(dbName)
    if not connection.open():
        return False
    createUserTable()
    return True
