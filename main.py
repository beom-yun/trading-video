import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from video import Video
from transaction import Transaction
from utils import *

### 파일위치(이름)
MAIN_WIDGET = "ui/mainWidget.ui"
DIALOG_VIDEO = "ui/dialogVideo.ui"
CANDLESTICK_ICON = "img/candlestick.png"
NEXT_SECU_ICON = "img/next-securities.png"
###

### 상수
DEFAULT_OFFSET = 5
###

# UI 파일 가져오기
form_class = uic.loadUiType(MAIN_WIDGET)[0]
dlg_video = uic.loadUiType(DIALOG_VIDEO)[0]


class DialogVideo(QDialog, dlg_video):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.dialog_accepted)
        self.video_start_time = None

    def dialog_accepted(self):
        self.video_start_time = self.dateTimeEdit.text()
        self.close()


class MainWidget(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

        self.v = Video()
        self.tr = Transaction()

    def initUi(self):
        # 윈도우아이콘, 로고 설정
        self.setWindowIcon(QIcon(CANDLESTICK_ICON))
        self.lbl_logo.setPixmap(QPixmap(NEXT_SECU_ICON))

        # '파일 열기', '초기화', '전체선택' '만들기' 버튼 클릭
        self.btn_open_file.clicked.connect(self.open_file)
        self.btn_rst_file.clicked.connect(self.reset_file)
        self.btn_all_check.clicked.connect(self.btn_all_check_clicked)
        self.btn_make.clicked.connect(self.btn_make_clicked)

    # '파일 열기' 버튼 클릭
    def open_file(self):
        # 녹화영상 파일 체크
        video_file = QFileDialog.getOpenFileName(
            self, caption="녹화영상 파일 선택", filter="mp4 file(*.mp4)"
        )
        if not video_file[0]:
            return

        res_v = self.v.open_video(video_file[0])
        if not res_v["ok"]:
            print("video open error")
            ##### 에러발생 다이얼로그 필요 #####
            return

        # 영상 시작시간 설정
        # 파일명으로 시작시간을 알 수 없다면, dialog로 직접 입력받음
        accepted = True
        if res_v["datetime"]:
            self.lbl_video_start_time.setText(res_v["datetime_str"])
        else:
            dlg = DialogVideo()
            accepted = bool(dlg.exec_())
            self.lbl_video_start_time.setText(dlg.video_start_time)
        if not accepted:
            return

        # 파일명, 영상길이 label 입력
        self.lbl_video_file.setText(res_v["file_name"])
        self.lbl_video_duration.setText(seconds_to_str(res_v["duration"]))

        # 거래내역 파일 체크
        csv_file = QFileDialog.getOpenFileName(
            self, caption="거래내역 파일 선택", filter="csv file(*.csv)"
        )
        if not csv_file[0]:
            return

        res_tr = self.tr.open_tr(csv_file[0])
        if not res_tr["ok"]:
            print("transaction open error")
            ##### 에러발생 다이얼로그 필요 #####
            return

        # 파일명, 거래횟수 label 입력
        self.lbl_csv_file.setText(res_tr["file_name"])
        self.lbl_csv_cnt.setText(str(res_tr["count"]))

        # '파일 열기' 버튼 비활성화 / '전체선택', '문구 출력', '만들기' 활성화
        self.btn_open_file.setEnabled(False)
        self.btn_all_check.setEnabled(True)
        self.chk_text.setEnabled(True)
        self.btn_make.setEnabled(True)

        # list widget에 출력
        list_items = self.tr.list_data_to_str()
        for i in range(len(list_items)):
            list_items[i] = QListWidgetItem(list_items[i])
            list_items[i].setCheckState(False)
            self.list_widget.addItem(list_items[i])

    # '초기화' 버튼 클릭
    def reset_file(self):
        self.v.reset_video()

        # UI 초기화
        self.lbl_video_file.clear()
        self.lbl_video_duration.clear()
        self.lbl_video_start_time.clear()
        self.edit_offset_start.setValue(DEFAULT_OFFSET)
        self.edit_offset_end.setValue(DEFAULT_OFFSET)
        self.lbl_csv_file.clear()
        self.lbl_csv_cnt.clear()
        self.btn_open_file.setEnabled(True)
        self.btn_all_check.setEnabled(False)
        self.chk_text.setEnabled(False)
        self.chk_text.setChecked(False)
        self.list_widget.clear()
        self.btn_make.setEnabled(False)

    # '전체 선택' 버튼 클릭
    def btn_all_check_clicked(self):
        flag = True
        for i in range(self.list_widget.count()):
            flag &= bool(self.list_widget.item(i).checkState())

        # 전부다 체크 되어있다면 전부 체크해제
        if flag:
            for i in range(self.list_widget.count()):
                self.list_widget.item(i).setCheckState(0)
        # 하나라도 체크가 안 되어있다면 전부 체크
        else:
            for i in range(self.list_widget.count()):
                self.list_widget.item(i).setCheckState(2)

    # '만들기' 버튼 클릭
    def btn_make_clicked(self):
        checked = list()
        for i in range(self.list_widget.count()):
            if bool(self.list_widget.item(i).checkState()):
                checked.append(i)
        print(checked)
        ##### 영상 만들기!! #####


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = MainWidget()
    mainWidget.show()
    app.exec_()
