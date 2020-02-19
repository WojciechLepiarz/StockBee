from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QColor


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)

        self.dates = data["<DTYYYYMMDD>"].values
        self.open = data["<OPEN>"].values
        self.high = data["<HIGH>"].values
        self.low = data["<LOW>"].values
        self.close = data["<CLOSE>"].values
        self.volume = data["<VOL>"].values

        self.column_count = 6
        self.row_count = len(self.close)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Date", "Open", "High", "Low", "Close", "Volume")[section]
        else:
            return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                return "{:d}".format(int(self.dates[row]))
            elif column == 1:
                return "{:.2f}".format(self.open[row])
            elif column == 2:
                return "{:.2f}".format(self.high[row])
            elif column == 3:
                return "{:.2f}".format(self.low[row])
            elif column == 4:
                return "{:.2f}".format(self.close[row])
            elif column == 5:
                return "{:d}".format(int(self.volume[row]))
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None
