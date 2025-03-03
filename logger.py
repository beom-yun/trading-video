from proglog import ProgressBarLogger
from PyQt5.QtCore import QThread, pyqtSignal


class ProgressLoggerThread(QThread, ProgressBarLogger):
    valueChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]["total"]) * 100
        self.valueChanged.emit(int(percentage))
