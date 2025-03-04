from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

# 파일위치(이름)
DIALOG_VIDEO = "ui/dialogVideo.ui"
DIALOG_SELECT = "ui/dialogSelect.ui"

# UI 파일 가져오기
dlg_video = uic.loadUiType(DIALOG_VIDEO)[0]
dlg_select = uic.loadUiType(DIALOG_SELECT)[0]


class DialogText(QDialog, dlg_select):
    def __init__(self, title="", text=""):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(title)
        self.lbl.setText(text)


class DialogVideo(QDialog, dlg_video):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.dialog_accepted)
        self.video_start_time = None

    def dialog_accepted(self):
        self.video_start_time = self.dateTimeEdit.text()
        self.close()
