from datetime import datetime, timedelta
from moviepy import *

###
video_file = "2025-02-19 18-33-40.mp4"
transactions = [
    {
        "ticker": "GCJ25",
        "start_time": datetime(2025, 2, 19, 18, 33, 59),
        "end_time": datetime(2025, 2, 19, 18, 34, 20),
        "type": "매수",
        "pnl": -80,
        "fee": 28,
    },
    {
        "ticker": "GCJ25",
        "start_time": datetime(2025, 2, 19, 18, 34, 33),
        "end_time": datetime(2025, 2, 19, 18, 37, 2),
        "type": "매수",
        "pnl": -450,
        "fee": 70,
    },
]
offset_start = 5
offset_end = 5
###


def get_video_start_time(video: str):
    try:
        file_name = video.split(".")[0]
        return datetime.strptime(file_name, "%Y-%m-%d %H-%M-%S")
    except:
        return None


def is_in_the_video(start_time, end_time, transaction) -> bool:
    try:
        tr_s, tr_e = transaction["start_time"], transaction["end_time"]
        if start_time <= tr_s and tr_e <= end_time:
            return True
        else:
            return False
    except:
        return False


video = VideoFileClip(video_file)
print(video.reader.infos)
video_start_time = get_video_start_time(video_file)  # start time을 확실히 가져와야함
video_end_time = video_start_time + timedelta(seconds=video.duration)

video_clips = list()
for tr in transactions:
    # 트랜잭션이 해당 비디오 안에 포함이 되는지 체크
    if is_in_the_video(video_start_time, video_end_time, tr):
        s = tr["start_time"] - video_start_time - timedelta(seconds=offset_start)
        e = tr["end_time"] - video_start_time + timedelta(seconds=offset_end)
        s = str(max(s, timedelta(hours=0, minutes=0, seconds=0)))
        e = str(min(e, video_end_time - video_start_time))
        clip = video.subclipped(s, e)
        video_clips.append({**tr, "clip": clip})
    else:
        pass

for clip in video_clips:
    date = clip["start_time"].strftime("%Y-%m-%d")
    time = clip["start_time"].strftime("%H:%M:%S")
    real_pnl = clip["pnl"] - clip["fee"]
    if real_pnl >= 0:
        real_pnl = "".join(["승(+", str(real_pnl), ")"])
    else:
        real_pnl = "".join(["패(", str(real_pnl), ")"])
    file_name = " ".join([date, time, clip["ticker"], clip["type"], real_pnl]) + ".mp4"
    clip["clip"].write_videofile(file_name)
