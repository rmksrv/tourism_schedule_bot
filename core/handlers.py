from datetime import date, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from loguru import logger

from core.constants import BOT_NAME, BOT_GITHUB_REPO, Weekdays, BotCommands
from core.utils import beautified_schedule_response, is_bottom_week
from services.schedule_service import ScheduleService


def keyboard() -> types.ReplyKeyboardMarkup:
    k = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [cmd.value for cmd in BotCommands]
    k.add(*buttons)
    return k


async def cmd_start(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = (
        f"Привет, я бот {BOT_NAME}. Я создан, чтобы потешить эго моего создателя. А еще я могу "
        f"подсказать расписание для студентов бакалавров ИМОМИ направления \"Туризм\".\n"
        f"Если хотите поддержать проект - поставьте ⭐ репозиторию на Github: {BOT_GITHUB_REPO}"
    )
    await message.answer(ans, reply_markup=keyboard())
    logger.debug("Bot answered: " + repr(ans))



async def cmd_today_schedule(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')

    d = date.today()
    ans = f"Расписание на сегодня, <b>{d} ({Weekdays.from_date(d).value})</b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))

    ans = beautified_schedule_response(await ScheduleService().today_schedule(grade=3) or "Свободный день!")
    await message.answer(ans, reply_markup=keyboard())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_tomorrow_schedule(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')

    d = date.today() + timedelta(days=1)
    ans = f"Расписание на завтра, <b>{d} ({Weekdays.from_date(d).value})</b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))

    ans = beautified_schedule_response(await ScheduleService().tomorrow_schedule(grade=3)) or "Свободный день!"
    await message.answer(ans, reply_markup=keyboard())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_is_bottom_week(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = "<b><i>Да</i></b>" if is_bottom_week() else "<b><i>Нет</i></b>"
    await message.answer(ans, reply_markup=keyboard())
    logger.debug("Bot answered: " + repr(ans))


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cmd_start, commands=["start", "help"])
    dispatcher.register_message_handler(cmd_today_schedule, Text(equals=BotCommands.Today.value))
    dispatcher.register_message_handler(cmd_tomorrow_schedule, Text(equals=BotCommands.Tomorrow.value))
    dispatcher.register_message_handler(cmd_is_bottom_week, Text(equals=BotCommands.IsBottomWeek.value))
