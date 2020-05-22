from PyQt5.QtWidgets import (QToolBar, QWidget, QMainWindow,
                             QApplication, QAction, QFileDialog,
                             QDockWidget, QListWidget, QMenu,
                             QActionGroup, QDialog, QPushButton,
                             QComboBox, QGridLayout, QLineEdit,
                             QLabel, QListWidgetItem, QMessageBox,
                             QHBoxLayout, QVBoxLayout, QFrame,
                             QDoubleSpinBox, QRadioButton, QSplitter,
                             QTableView, QTableWidget, QTableWidgetItem,
                             QAbstractItemView, QPlainTextEdit)
from PyQt5.QtGui import QIcon, QRegExpValidator, QIntValidator, QDoubleValidator, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QSizePolicy
from abc import ABC
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd

import sys
import subprocess

from ui.canvas import DataOverviewWidget
from ui.data_table import FlowTable
from ui.rm_col_dlg import RmColDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "VizarD"

        # Line below fixed the issue of invisible menu bar running app in MacOS
        self.menuBar().setNativeMenuBar(False)

        self.setWindowTitle(title)
        self.overview_widget = None
        self._init_ui()

    def _init_ui(self):
        self._init_menus()
        self.init_plot()
        self._init_dockable()

    def _init_menus(self):
        self.save_prj_ui = SaveSessionUI()
        self.load_prj_ui = LoadSessionUI()
        self.open_file_ui = OpenFileUI()
        self.save_file_ui = SaveFileUI()
        self._init_file_menu()

    def init_plot(self):
        self.overview_widget = DataOverviewWidget(self)
        self.setCentralWidget(self.overview_widget)
        # # added navigation toolbar on figure canvas
        self.navi_toolbar = NavigationToolbar(self.overview_widget, self.overview_widget)

    def _init_dockable(self):
        # Remove column button
        bt_rm = QPushButton('Remove Column')
        bt_rm.setMaximumWidth(200)
        bt_rm.clicked.connect(self._call_rm_col)
        bt_rm.show()

        # Flow table widget
        self.t1 = QTableView()
        dock_bottom = QDockWidget('Imported data', self)
        dock_bottom.setAllowedAreas(Qt.AllDockWidgetAreas)
        # self.t1.setSelectionBehavior(QAbstractItemView.SelectRows)  # data table only allow row-selection
        self.t1.setSelectionMode(QAbstractItemView.NoSelection)  # Disable selection for data table

        # Layout of the dockable widget
        self.data_tab_frame = QFrame()
        vbox = QVBoxLayout()
        vbox.addWidget(bt_rm)
        vbox.addWidget(self.t1)
        self.data_tab_frame.setLayout(vbox)

        dock_bottom.setWidget(self.data_tab_frame)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock_bottom)

    def _call_rm_col(self):
        RmColDialog()

    def _init_file_menu(self):
        self._menu_file = self.menuBar().addMenu("&File")

        self._menu_file_save_project = QAction(QIcon(""), "Save Project", self)
        self._menu_file_save_project.triggered.connect(lambda: self.save_prj_ui.init_dialog(self))
        self._menu_file.addAction(self._menu_file_save_project)

        self._menu_file_load_project = QAction(QIcon(""), "Load Project", self)
        self._menu_file_load_project.triggered.connect(lambda: self.load_prj_ui.init_dialog(self))
        self._menu_file.addAction(self._menu_file_load_project)

        self._menu_file.addSeparator()

        self._menu_file_import_data = QAction(QIcon(""), "Import Data File", self)
        self._menu_file_import_data.triggered.connect(lambda: self.open_file_ui.init_dialog(self))
        self._menu_file.addAction(self._menu_file_import_data)

        self._menu_file_export_csv = QAction(QIcon(""), "Export Data File", self)
        self._menu_file_export_csv.triggered.connect(lambda: self.save_file_ui.init_dialog(self))
        self._menu_file.addAction(self._menu_file_export_csv)

        self._menu_file.addSeparator()

    def data_tb_upd(self):
        self.data_tb = FlowTable(self.t1)


class FileMenuUI(ABC):
    def init_dialog(self):
        pass


class OpenFileUI(FileMenuUI):
    def init_dialog(self, main_window):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(main_window, "QFileDialog.getOpenFileName()", "",
                                                     "csv files (*.csv)", options=options)
        if file_names:
            QApplication.instance().datasetmng.sig_imp_from_file.emit(file_names)


class SaveFileUI(FileMenuUI):
    def init_dialog(self, main_window):
        pass


class SessionUI(ABC):
    def init_dialog(self):
        pass


class SaveSessionUI(SessionUI):
    def init_dialog(self, main_window):
        pass


class LoadSessionUI(SessionUI):
    def init_dialog(self, main_window):
        pass
