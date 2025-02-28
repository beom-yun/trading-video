from datetime import datetime
from moviepy import *


class Video:
    def __init__(self):
        self.data = None

    # mainWidget에서 '파일 열기' 동작
    def open_video(self, file):
        try:
            name = file.split("/")[-1]
            self.data = VideoFileClip(file)

            try:
                dt = datetime.strptime(name.split(".")[0], "%Y-%m-%d %H-%M-%S")
                dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                dt = None
                dt_str = None

            return {
                "ok": True,
                "file_name": name,  # 파일명
                "duration": self.data.duration,  # 영상길이
                "datetime": dt,  # 영상 시작시간
                "datetime_str": dt_str,  # 영상 시작시간
            }
        except:
            return {
                "ok": False,
                "file_name": "",
                "duration": 0,
                "datetime": None,
                "datetime_str": None,
            }

    # mainWidget에서 '초기화' 동작
    def reset_video(self):
        self.data = None
