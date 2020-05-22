from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton,
                             QComboBox, QGridLayout, QLabel)
from PyQt5.QtCore import Qt

# ui.data_summary_widget import TableUpdateTrigger
from processing.datamng import DataManipulate
from ui.data_table import TableUpdateTrigger


class RmColDialog():
    def __init__(self):
        self.dialog = None
        self.datasetmng = QApplication.instance().datasetmng
        self.col_name = []

        self._init_dialog()

    def _init_dialog(self):
        self.dialog = QDialog()

        lb_description = QLabel("Select the column you want to remove:")

        # TODO: Combobox is no better than list widget items in this scenario, need to optimize
        cb_label = QComboBox()
        cb_label.addItems(self.datasetmng.get_dataset().columns)

        bt_ok = QPushButton('Remove', self.dialog)
        bt_ok.show()
        bt_cancel = QPushButton('Cancel', self.dialog)

        layout_grid = QGridLayout()
        layout_grid.setSpacing(10)
        layout_grid.addWidget(lb_description, 0, 1, 1, 2)
        layout_grid.addWidget(cb_label, 1, 1, 1, 2)
        layout_grid.addWidget(bt_cancel, 2, 1, 1, 1)
        layout_grid.addWidget(bt_ok, 2, 2, 1, 1)

        bt_ok.clicked.connect(lambda: self._rm_col(cb_label.currentText()))
        bt_cancel.clicked.connect(self._cancel)

        self.dialog.setLayout(layout_grid)

        self.dialog.setWindowTitle("Remove Selected Columns")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def _rm_col(self, col_name):
        DataManipulate(self.datasetmng.get_dataset()).rm_col(col_name)

        TableUpdateTrigger().data_changed_trigger()

        self.dialog.close()

    def _cancel(self):
        self.dialog.close()

