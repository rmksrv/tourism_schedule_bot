from datetime import date
from typing import Dict, Optional


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def is_bottom_week(d: date = date.today()) -> bool:
    return int(d.strftime("%V")) % 2 == 0


def beautified_schedule_response(schedule: Dict[str, Optional[str]]) -> str:
    response = ""

    for time, lesson in schedule.items():
        if not lesson:
            continue
        response += f"<b>{time.replace('.', ':')}</b>\n" f"<i>{lesson}</i>\n\n"

    return response
