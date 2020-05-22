import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import pandas as pd
from abc import ABC

import os
import ast
import logging
import csv
import pickle
import sys
import hashlib  # due to Python3 will change hash seed every time restarts the session, use hashlib instead
import ntpath

logger = logging.getLogger(__name__)

from .constants import *

class DatasetManager(QObject):
    sig_imp_from_file = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.master_dataset = pd.DataFrame()
        self.filtered_dataset = pd.DataFrame()
        self.df_sampled = pd.DataFrame()
        self.importers = CSVImporter()
        self.exporters = CSVExporter()

        self.sample_size = SAMPLE_SIZE

        # Connect signals to slot
        self.sig_imp_from_file.connect(self.impt_from_file)

        self.f_list = []
        self.plot_dict = None

    @pyqtSlot(list)
    def impt_from_file(self, fnames):
        self.master_dataset = QApplication.instance().datasetmng.import_dataset(fnames)
        QApplication.instance().mainWindow.data_tb_upd()

    def import_dataset(self, file_names):
        # Concat newly imported data to previous dataset
        for f in file_names:
            self._concat_files(f)

        # Consider to reindex the dataset before processing anything else, due to duplicate ind by multi-file import
        self.master_dataset = self.master_dataset.reset_index(drop=True)

        return self.master_dataset

    def _concat_files(self, file_name):
        self.master_dataset = pd.concat([self.master_dataset, self.importers.import_data(file_name)], sort=False)

    def get_dataset(self):
        return self.master_dataset


class DataManipulate():
    def __init__(self, data):
        self.dataset = data

    def rm_col(self, col_name):
        return self.dataset.drop(col_name, axis=1)


class DatasetImporter(ABC):  # abstract class
    def import_data(self):
        pass


class CSVImporter(DatasetImporter):
    def import_data(self, file_name):
        return pd.read_csv(file_name, index_col=0)


class DatasetExporter(ABC):
    def export_data(self):
        pass


class CSVExporter(DatasetExporter):
    def export_data(self, file_name):
        QApplication.instance().datasetmng.get_dataset().to_csv(file_name)
