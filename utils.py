import math
from datetime import datetime


# 입력 : 초(float) / 출력 : 'OO시간 OO분 OO초'(str)
def seconds_to_str(seconds: float) -> str:
    try:
        seconds = math.ceil(seconds)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        return " ".join(
            [
                f"{str(hours)}시간" if hours else "",
                f"{str(minutes)}분" if minutes else "",
                f"{str(seconds)}초" if seconds else "",
            ]
        ).strip()
    except:
        return ""


def str_to_datetime(string: str, format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    return datetime.strptime(string, format)


def datetime_to_str(datetime: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.strftime(format)
