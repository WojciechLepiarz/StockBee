import requests
import zipfile
import pandas as pd
from PySide2.QtCore import Slot, qApp
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Eartquakes information")
        self.setCentralWidget(widget)

        # Setup links
        link_data = pd.read_csv("stockbee/databases.csv", header=0, index_col=0)
        self.full_link = link_data.loc["full"][0]
        self.partial_link = link_data.loc["latest"][0]

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        get_partial_data_action = QAction("Get latest date", self)
        get_partial_data_action.triggered.connect(self.get_partial_data)
        get_full_data_action = QAction("Get all available data", self)
        get_full_data_action.triggered.connect(self.get_full_data)
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(get_partial_data_action)
        self.file_menu.addAction(get_full_data_action)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(int(geometry.width() * 0.8),
                          int(geometry.height() * 0.7))

    def get_partial_data(self) -> None:
        myfile = requests.get(self.partial_link)
        with open('last_data.zip', 'wb') as ff:
            ff.write(myfile.content)
        self.status.showMessage("I got latest data for you!")

    def get_full_data(self) -> None:
        myfile = requests.get(self.full_link)
        with open('full_data.zip', 'wb') as ff:
            ff.write(myfile.content)
        self.status.showMessage("I got full data for you!")
