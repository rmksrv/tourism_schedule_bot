from datetime import date
from enum import Enum


BOT_NAME = "TourismSchedule"
BOT_USERNAME = "tourism_schedule_bot"
BOT_GITHUB_REPO = r"https://github.com/rmksrv/tourism_schedule_bot"

IMOMI_ROOT_URL = r"http://www.imomi.unn.ru"
IMOMI_SCHEDULES_PAGE_URL = r"http://www.imomi.unn.ru/education/raspisanie-zanyatiy"


class BotCommands(Enum):
    Today = "Сегодня"
    Tomorrow = "Завтра"
    IsBottomWeek = "Эта неделя нижняя?"
    ChangeGrade = "Сменить курс"
    # Monday = "Понедельник"
    # Tuesday = "Вторник"
    # Wednesday = "Среда"
    # Thursday = "Четверг"
    # Friday = "Пятница"
    # Saturday = "Суббота"


class Weekdays(Enum):
    Monday = "ПОНЕДЕЛЬНИК"
    Tuesday = "ВТОРНИК"
    Wednesday = "СРЕДА"
    Thursday = "ЧЕТВЕРГ"
    Friday = "ПЯТНИЦА"
    Saturday = "СУББОТА"
    Sunday = "ВОСКРЕСЕНЬЕ"

    @classmethod
    def from_date(cls, d: date):
        weekday = d.weekday() + 1
        if weekday == 1:
            return Weekdays.Monday
        elif weekday == 2:
            return Weekdays.Tuesday
        elif weekday == 3:
            return Weekdays.Wednesday
        elif weekday == 4:
            return Weekdays.Thursday
        elif weekday == 5:
            return Weekdays.Friday
        elif weekday == 6:
            return Weekdays.Saturday
        elif weekday == 7:
            return Weekdays.Sunday
