from datetime import datetime
from moviepy import *


class Video:
    def __init__(self):
        self.file = None

    def open_video(self, file):
        self.file = file
        file_name = file.split("/")[-1]

        try:
            dt = datetime.strptime(file_name.split(".")[0], "%Y-%m-%d %H-%M-%S")
        except:
            dt = None

        return {
            "file_name": file_name,
            "datetime": dt,
        }
