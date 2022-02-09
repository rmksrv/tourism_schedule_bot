import pathlib

from core.daily_schedule import DailyScheduleParser

if __name__ == "__main__":
    schedule_file = pathlib.Path("Туризм.docx")
    s = DailyScheduleParser(schedule_file)
    # schedule = s.daily_schedule(date.today(), 3)
    schedule = s.tomorrow_schedule(3)
    assert True
