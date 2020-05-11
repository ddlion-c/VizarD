from PyQt5.QtWidgets import QSizePolicy, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from matplotlib.widgets import LassoSelector, RectangleSelector
from matplotlib.path import Path
from matplotlib import cm
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from abc import ABC

import numpy as np


class DataOverviewWidget(FigureCanvas):
    def __init__(self, parent=None):
        figure = Figure(figsize=(5, 4), dpi=100)
        self.axes = figure.add_subplot(111)

        super().__init__(figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # Add setFocus to fix keypress not working issue
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)

        self.axes.axis('off')
        self.axes.set_title('VizarD')


