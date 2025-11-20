from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from digipage.data.io import LogManager
from datetime import datetime

class LogViewerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log Viewer")
        self.resize(800, 600)
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Book Name", "Pages", "Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.refresh_btn)

        self.load_data()

    def load_data(self):
        logs = LogManager.load_logs()
        self.table.setRowCount(0)

        row = 0
        for date_str, entries in logs.items():
            for entry in entries:
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(date_str))
                self.table.setItem(row, 1, QTableWidgetItem(entry.get("name", "")))
                self.table.setItem(row, 2, QTableWidgetItem(str(entry.get("pages", 0))))
                self.table.setItem(row, 3, QTableWidgetItem(entry.get("path", "")))
                row += 1
