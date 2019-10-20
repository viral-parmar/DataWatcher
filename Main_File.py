import os
import pandas as pd
from PyQt5 import QtCore, QtWidgets
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from Append_Function import append_df_to_excel
import time


class Emitter(QtCore.QObject):
    newDataFrameSignal = QtCore.pyqtSignal(pd.DataFrame)


class Watcher:
    def __init__(self):
        self.watch_dir = os.getcwd()
        self.directory_to_watch = None
        self.emitter = Emitter()
        self.observer = Observer()
        self.event_handler = Handler(
            emitter=self.emitter,
            patterns=["*.CSV"],
            ignore_patterns=["*.tmp"],
            ignore_directories=True
        )

    def set_filename(self, filename):
        self.directory_to_watch = os.path.join(self.watch_dir, filename)

    def run(self):
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=False)
        self.observer.start()

    def stop_watcher(self):
        self.observer.stop()


class Handler(PatternMatchingEventHandler):
    def __init__(self, *args, emitter=None, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self._emitter = emitter
        self.file_name = time.strftime("%Y%m%d-%H%M%S")+".xlsx"

    def on_any_event(self, event):

        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

            if os.path.isfile(os.path.join(os.getcwd(), self.file_name)):
                time.sleep(.300)
                append_df_to_excel(os.path.join(os.getcwd(), self.file_name),
                                   pd.read_csv(event.src_path, header=1, index_col=0))
                df = pd.read_csv(event.src_path, header=1)

            else:
                time.sleep(.300)
                append_df_to_excel(os.path.join(os.getcwd(), self.file_name),
                                   pd.read_csv(event.src_path, header=0, index_col=0))

                df = pd.read_csv(event.src_path, header=0)

            self._emitter.newDataFrameSignal.emit(df.copy())
            df.set_index(df.columns.values.tolist()[0], inplace=True)

        elif event.event_type == 'modified':
            print("Modified created event - %s." % event.src_path)

            if os.path.isfile(os.path.join(os.getcwd(), self.file_name)):
                time.sleep(.300)
                append_df_to_excel(os.path.join(os.getcwd(), self.file_name),
                                   pd.read_csv(event.src_path, header=1, index_col=0))
                df = pd.read_csv(event.src_path, header=1)

            else:
                time.sleep(.300)
                append_df_to_excel(os.path.join(os.getcwd(), self.file_name),
                                   pd.read_csv(event.src_path, header=0, index_col=0),)
                df = pd.read_csv(event.src_path, header=0)

            self._emitter.newDataFrameSignal.emit(df.copy())
            df.set_index(df.columns.values.tolist()[0], inplace=True)


class DataFrameTableWidget(QtWidgets.QTableWidget):

    @QtCore.pyqtSlot(pd.DataFrame)
    def append_dataframe(self, df):
        df = df.copy()
        if df.columns.size > self.columnCount():
            self.setColumnCount(df.columns.size)
        r = self.rowCount()
        self.insertRow(r)
        for c, column in enumerate(df):
            it = QtWidgets.QTableWidgetItem(column)

            self.setItem(r, c, it)
        i = self.rowCount()
        for r, row in df.iterrows():
            self.insertRow(self.rowCount())
            for c, (column, value) in enumerate(row.iteritems()):
                it = QtWidgets.QTableWidgetItem(str(value))
                self.setItem(i+r, c, it)


