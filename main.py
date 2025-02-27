import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic


MAIN_WIDGET = "ui/mainWidget.ui"
CANDLESTICK_ICON = "img/candlestick.png"
NEXT_SECU_ICON = "img/next-securities.png"


# UI 파일 가져오기
form_class = uic.loadUiType(MAIN_WIDGET)[0]


class MainWidget(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.setWindowIcon(QIcon(CANDLESTICK_ICON))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = MainWidget()
    mainWidget.show()
    app.exec_()
