from datetime import date, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from loguru import logger

from core.constants import BOT_NAME, BOT_GITHUB_REPO, Weekdays, BotCommands
from core.utils import beautified_schedule_response, is_bottom_week
from services.schedule_service import ScheduleService

available_grades = [str(i + 1) for i in range(4)]


class UserInfo(StatesGroup):
    waiting_for_grade = State()
    grade_defined = State()


def keyboard_commands() -> types.ReplyKeyboardMarkup:
    k = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [c.value for c in BotCommands]
    k.add(*buttons)
    return k


def keyboard_available_grades() -> types.ReplyKeyboardMarkup:
    k = types.ReplyKeyboardMarkup(resize_keyboard=True)
    k.add(*available_grades)
    return k


async def cmd_start(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = (
        f"Привет, я бот {BOT_NAME}. Я создан, чтобы потешить эго моего создателя. А еще я могу "
        f'подсказать расписание для студентов бакалавров ИМОМИ направления "Туризм".\n'
        f"Если хотите поддержать проект - поставьте ⭐ репозиторию на Github: {BOT_GITHUB_REPO}"
    )
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))
    await grade_start(message, state)


async def grade_start(message: types.Message, state: FSMContext):
    await state.finish()
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = "Пожалуйста, укажи курс, на котором ты учишься:"
    await message.answer(ans, reply_markup=keyboard_available_grades())
    await UserInfo.waiting_for_grade.set()
    logger.debug("Bot answered: " + repr(ans))


async def grade_chosen(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    if message.text not in available_grades:
        ans = "Пожалуйста, укажи курс, на котором ты учишься используя клавиатуру снизу:"
        await message.answer(ans)
        logger.debug("Bot answered: " + repr(ans))
        return

    await UserInfo.grade_defined.set()
    await state.update_data(grade=message.text)

    ans = "Спасибо! Можешь пользоваться ботом!"
    await message.answer(ans, reply_markup=keyboard_commands())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_help(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = (
        f"Привет, я бот {BOT_NAME}. Я создан, чтобы потешить эго моего создателя. А еще я могу "
        f'подсказать расписание для студентов бакалавров ИМОМИ направления "Туризм".\n'
        f"Если хотите поддержать проект - поставьте ⭐ репозиторию на Github: {BOT_GITHUB_REPO}"
    )
    if state == UserInfo.grade_defined:
        await message.answer(ans, reply_markup=keyboard_commands())
    else:
        await message.answer(ans)
        await grade_start(message)
    logger.debug("Bot answered: " + repr(ans))


async def cmd_today_schedule(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')

    d = date.today()
    user_data = await state.get_data()
    grade = int(user_data.get("grade"))
    ans = f"Расписание для {grade} курса на сегодня, <b>{d} ({Weekdays.from_date(d).value})</b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))

    ans = beautified_schedule_response(await ScheduleService().today_schedule(grade) or "Свободный день!")
    await message.answer(ans, reply_markup=keyboard_commands())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_tomorrow_schedule(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')

    d = date.today() + timedelta(days=1)
    ans = f"Расписание на завтра, <b>{d} ({Weekdays.from_date(d).value})</b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))

    ans = beautified_schedule_response(await ScheduleService().tomorrow_schedule(grade=3)) or "Свободный день!"
    await message.answer(ans, reply_markup=keyboard_commands())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_is_bottom_week(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = "<b><i>Да</i></b>" if is_bottom_week() else "<b><i>Нет</i></b>"
    await message.answer(ans, reply_markup=keyboard_commands())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_change_grade(message: types.Message, state: FSMContext):
    await grade_start(message, state)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cmd_start, commands=["start"], state="*")
    dispatcher.register_message_handler(cmd_help, commands=["help"], state="*")
    dispatcher.register_message_handler(grade_chosen, state=UserInfo.waiting_for_grade)
    dispatcher.register_message_handler(
        cmd_today_schedule, Text(equals=BotCommands.Today.value), state=UserInfo.grade_defined
    )
    dispatcher.register_message_handler(
        cmd_tomorrow_schedule, Text(equals=BotCommands.Tomorrow.value), state=UserInfo.grade_defined
    )
    dispatcher.register_message_handler(
        cmd_is_bottom_week, Text(equals=BotCommands.IsBottomWeek.value), state=UserInfo.grade_defined
    )
    dispatcher.register_message_handler(
        cmd_change_grade, Text(equals=BotCommands.ChangeGrade.value), state=UserInfo.grade_defined
    )
