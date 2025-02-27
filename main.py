import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from video import Video

### 파일위치(이름)
MAIN_WIDGET = "ui/mainWidget.ui"
CANDLESTICK_ICON = "img/candlestick.png"
NEXT_SECU_ICON = "img/next-securities.png"
###

# UI 파일 가져오기
form_class = uic.loadUiType(MAIN_WIDGET)[0]


class MainWidget(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

        self.v = Video()

    def initUi(self):
        # 윈도우아이콘, 로고 설정
        self.setWindowIcon(QIcon(CANDLESTICK_ICON))
        self.lbl_logo.setPixmap(QPixmap(NEXT_SECU_ICON))

        # '파일 열기', '초기화' 버튼 클릭
        self.btn_open_file.clicked.connect(self.open_file)
        self.btn_rst_file.clicked.connect(self.reset_file)

    # '파일 열기' 버튼 클릭
    def open_file(self):
        video_file = QFileDialog.getOpenFileName(
            self, caption="녹화영상 파일 선택", filter="mp4 file(*.mp4)"
        )
        if not video_file[0]:
            return
        csv_file = QFileDialog.getOpenFileName(
            self, caption="거래내역 파일 선택", filter="csv file(*.csv)"
        )
        if not csv_file[0]:
            return

        # 녹화영상 파일 체크
        res = self.v.open_video(video_file[0])
        print(res)

        # 거래내역 파일 체크

    # '초기화' 버튼 클릭
    def reset_file(self):
        print("녹화영상, 거래내역 삭제")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = MainWidget()
    mainWidget.show()
    app.exec_()
