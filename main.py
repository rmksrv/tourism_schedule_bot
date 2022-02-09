import pathlib

from core.constants import Days
from core.day_schedule import DaySchedule

if __name__ == "__main__":
    schedule_file = pathlib.Path("Туризм.docx")
    s = DaySchedule(grade=2, day=Days.Wednesday)
    my_cells = s.cells_from_docx(schedule_file)
    my_schedule = s.formatted_schedule(schedule_file)
    assert True
