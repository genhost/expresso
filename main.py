import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QTableWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

HEADINGS = map(
    str.capitalize,
    (
        "ID",
        "название сорта",
        "степень обжарки",
        "молотый/в зернах",
        "описание вкуса",
        "цена",
        "объем упаковки",
    ),
)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table: QTableWidget

        uic.loadUi("main.ui", self)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(HEADINGS)

        self.setCentralWidget(self.table)

        self.loadTable()

    def loadTable(self):
        with sqlite3.connect("coffee.sqlite") as con:
            cur = con.cursor()
            rows = cur.execute("SELECT * FROM coffees").fetchall()

            for i, row in enumerate(rows):
                self.table.setRowCount(self.table.rowCount() + 1)

                for j, elem in enumerate(row):
                    elem = str(elem)

                    if elem == "true":
                        elem = "Молотый"
                    elif elem == "false":
                        elem = "В зернах"

                    self.table.setItem(i, j, QTableWidgetItem(elem))

        self.table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
