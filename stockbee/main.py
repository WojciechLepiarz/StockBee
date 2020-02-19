import sys
import argparse
import pandas as pd

from PySide2.QtCore import QDateTime, QTimeZone
from PySide2.QtWidgets import QApplication
from stockbee.objects.main_window import MainWindow
from stockbee.objects.central_widget import CentralWidget


if __name__ == "__main__":
    options = argparse.ArgumentParser()
    options.add_argument("-f", "--file", type=str, required=False)
    args = options.parse_args()
    data = pd.read_csv("stock_data/WIG.mst")

    # Qt Application
    app = QApplication(sys.argv)

    widget = CentralWidget(data)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())
