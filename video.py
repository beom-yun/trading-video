from datetime import timedelta
from moviepy import *
from utils import str_to_datetime, datetime_to_str


##### ToDo : 클립 영상에 text 추가하기 #####


class Video:
    def __init__(self):
        self.data = None

    # mainWidget에서 '파일 열기' 동작
    def open_video(self, file):
        try:
            name = file.split("/")[-1]
            self.data = VideoFileClip(file)

            try:
                dt = str_to_datetime(name.split(".")[0], "%Y-%m-%d %H-%M-%S")
                dt_str = datetime_to_str(dt)
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

    # listWidget으로부터 체크된 데이터 입력, 비디오클립 출력
    # data: 트랜잭션 / text: 문구 / start_time: 영상시작시간 / offset_start: 오프셋 시작 / offset_end: 오프셋 끝
    def make_video(self, data, text, start_time, offset_start, offset_end, logger):
        video_start_time = str_to_datetime(start_time)
        video_end_time = video_start_time + timedelta(seconds=self.data.duration)
        if self.is_in_the_video(video_start_time, video_end_time, data):
            s = data["start_time"] - video_start_time - timedelta(seconds=offset_start)
            e = data["end_time"] - video_start_time + timedelta(seconds=offset_end)
            s = str(max(s, timedelta(hours=0, minutes=0, seconds=0)))
            e = str(min(e, video_end_time - video_start_time))
            clip = self.data.subclipped(s, e)

            real_pnl = data["pnl"] - data["fee"]
            if real_pnl >= 0:
                real_pnl = "".join(["승(+", str(real_pnl), ")"])
            else:
                real_pnl = "".join(["패(", str(real_pnl), ")"])
            file_name = f'{datetime_to_str(data["start_time"], "%y%m%d-%H%M%S")} {data["ticker"]} {data["type"]} {real_pnl}.mp4'
            clip.write_videofile(file_name, logger=logger)

    # 해당 트랜잭션이 비디오 안에 포함되어 있는지 체크
    def is_in_the_video(self, start_time, end_time, transaction) -> bool:
        try:
            if (
                start_time <= transaction["start_time"]
                and transaction["end_time"] <= end_time
            ):
                return True
            else:
                return False
        except:
            return False

    # mainWidget에서 '초기화' 동작
    def reset_video(self):
        self.data = None
