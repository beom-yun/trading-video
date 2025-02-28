from datetime import datetime
from moviepy import *


class Video:
    def __init__(self):
        self.data = None

    # mainWidget에서 '파일 열기' 동작
    def open_video(self, file):
        name = file.split("/")[-1]
        self.data = VideoFileClip(file)

        try:
            dt = datetime.strptime(name.split(".")[0], "%Y-%m-%d %H-%M-%S")
        except:
            dt = None

        return {
            "file_name": name,  # 파일명
            "duration": self.data.duration,  # 영상길이
            "datetime": dt,  # 영상 시작시간
        }
