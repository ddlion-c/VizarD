from PyQt5.QtWidgets import (QTableWidgetItem, QApplication)
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QObject, QAbstractTableModel
from PyQt5 import QtGui, QtWidgets
from collections import Counter

import pandas as pd
from operator import itemgetter
import numpy as np
import time
from abc import ABC


# Todo: The data type of data table is not correct, need to fix it
class DataFrameModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data.copy()

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._data.columns[section]
            else:
                return str(self._data.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()


class FlowTable:
    def __init__(self, widget):
        self.datasetmng = QApplication.instance().datasetmng

        df = self.datasetmng.get_dataset()

        model = DataFrameModel(df)
        self.widget = widget
        self.widget.setModel(model)

        # Below two lines have same effect, resize the columns to content width, but resize mode will freeze resize func
        self.widget.resizeColumnsToContents()
        # self.widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def refresh_data(self):
        df = self.datasetmng.get_dataset()
        model = DataFrameModel(df)
        self.widget.setModel(model)

        self.widget.resizeColumnsToContents()


"""
Trigger format: signal emit embedded in a trigger method
One signal can connect to multiple event methods
"""


class TableUpdateTrigger(QObject):
    selection_changed = pyqtSignal()
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.get_ind = None
        self.datasetmng = QApplication.instance().datasetmng
        self.data_tb = QApplication.instance().mainWindow.data_tb
        self.data_changed.connect(self.flow_tb_refresh)

    def data_changed_trigger(self):
        self.data_changed.emit()

    def flow_tb_refresh(self):
        self.data_tb.refresh_data()


