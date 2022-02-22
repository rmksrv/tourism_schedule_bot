from datetime import date, timedelta

from aiogram import types, Dispatcher
from loguru import logger

from core.constants import BOT_NAME, Weekdays
from core.utils import beautified_schedule_response, is_bottom_week
from services.schedule_service import ScheduleService


async def cmd_start(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    # TODO: сделать мсг получше
    ans = (
        f"Привет, я бот {BOT_NAME}. Я создан, чтобы потешить эго моего создателя. А еще я могу "
        f"подсказать расписание на сегодня или завтра."
    )
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))


async def cmd_today_schedule(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')

    d = date.today()
    ans = f"Расписание на сегодня, <b>{d} ({Weekdays.from_date(d).value})</b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))

    ans = beautified_schedule_response(await ScheduleService().today_schedule(grade=3) or "Свободный день!")
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))


async def cmd_tomorrow_schedule(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')

    d = date.today() + timedelta(days=1)
    ans = f"Расписание на завтра, <b>{d} ({Weekdays.from_date(d).value})</b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))

    ans = beautified_schedule_response(await ScheduleService().tomorrow_schedule(grade=3)) or "Свободный день!"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))


async def cmd_is_bottom_week(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = "<b><i>Да</i></b>" if is_bottom_week() else "<b><i>Нет</i></b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cmd_start, commands=["start", "help"])
    dispatcher.register_message_handler(cmd_today_schedule, commands=["today_schedule"])
    dispatcher.register_message_handler(cmd_tomorrow_schedule, commands=["tomorrow_schedule"])
    dispatcher.register_message_handler(cmd_is_bottom_week, commands=["is_bottom_week"])
