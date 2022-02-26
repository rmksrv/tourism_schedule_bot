import asyncio
from datetime import date, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from loguru import logger

from core.bot import bot, bot_token
from core.constants import BOT_NAME, BOT_GITHUB_REPO, Weekdays, UserCommands, AdminCommands
from core.utils import beautified_schedule_response, is_bottom_week
from services.schedule_service import ScheduleService

available_grades = [str(i + 1) for i in range(4)]


def keyboard_admin_commands() -> types.ReplyKeyboardMarkup:
    k = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [c.value for c in AdminCommands]
    k.add(*buttons)
    return k


def keyboard_user_commands() -> types.ReplyKeyboardMarkup:
    k = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [c.value for c in UserCommands]
    k.add(*buttons)
    return k


def keyboard_available_grades() -> types.ReplyKeyboardMarkup:
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    k.add(*available_grades)
    return k


class UserState(StatesGroup):
    waiting_for_grade = State()
    grade_defined = State()
    admin_mode_menu = State()
    admin_mode_broadcast_message_waiting = State()


async def grade_start(message: types.Message, state: FSMContext):
    await state.finish()
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = "Пожалуйста, укажи курс, на котором ты учишься:"
    await message.answer(ans, reply_markup=keyboard_available_grades())
    await UserState.waiting_for_grade.set()
    logger.debug("Bot answered: " + repr(ans))


async def grade_chosen(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    if message.text not in available_grades:
        ans = "Пожалуйста, укажи курс, на котором ты учишься используя клавиатуру снизу:"
        await message.answer(ans)
        logger.debug("Bot answered: " + repr(ans))
        return

    await UserState.grade_defined.set()
    await state.update_data(grade=message.text)

    ans = "Спасибо! Можешь пользоваться ботом!"
    await message.answer(ans, reply_markup=keyboard_user_commands())
    logger.debug("Bot answered: " + repr(ans))


async def token_passed(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    await UserState.admin_mode_menu.set()
    ans = f"Доступ подтвержден пользователю {message.from_user.username}!"
    await message.answer(ans, reply_markup=keyboard_admin_commands())
    logger.debug("Bot answered: " + repr(ans))


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


async def cmd_help(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = (
        f"Привет, я бот {BOT_NAME}. Я создан, чтобы потешить эго моего создателя. А еще я могу "
        f'подсказать расписание для студентов бакалавров ИМОМИ направления "Туризм".\n'
        f"Если хотите поддержать проект - поставьте ⭐ репозиторию на Github: {BOT_GITHUB_REPO}"
    )
    if state == UserState.grade_defined:
        await message.answer(ans, reply_markup=keyboard_user_commands())
    else:
        await message.answer(ans)
        await grade_start(message, state)
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
    await message.answer(ans, reply_markup=keyboard_user_commands())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_tomorrow_schedule(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')

    d = date.today() + timedelta(days=1)
    ans = f"Расписание на завтра, <b>{d} ({Weekdays.from_date(d).value})</b>"
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))

    ans = beautified_schedule_response(await ScheduleService().tomorrow_schedule(grade=3)) or "Свободный день!"
    await message.answer(ans, reply_markup=keyboard_user_commands())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_is_bottom_week(message: types.Message):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = "<b><i>Да</i></b>" if is_bottom_week() else "<b><i>Нет</i></b>"
    await message.answer(ans, reply_markup=keyboard_user_commands())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_change_grade(message: types.Message, state: FSMContext):
    await grade_start(message, state)


async def cmd_broadcast_start(message: types.Message, state: FSMContext):
    logger.debug(f'User @{message.from_user.username} sent "{message.text}"')
    ans = "Введи текст, который хочешь отправить"
    await UserState.admin_mode_broadcast_message_waiting.set()
    await message.answer(ans, reply_markup=types.ReplyKeyboardMarkup())
    logger.debug("Bot answered: " + repr(ans))


async def cmd_broadcast_send(message: types.Message, state: FSMContext):
    count = 0
    try:
        for user_id in get_users(state):
            if await send_message(user_id, message.text):
                count += 1
            await asyncio.sleep(.05)
    finally:
        logger.info(f"{count} messages sent successfully!")

    await UserState.admin_mode_menu.set()
    ans = "Готово! Сообщение доставлено пользователям бота."
    await message.answer(ans)
    logger.debug("Bot answered: " + repr(ans))


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False


def get_users(state: FSMContext):
    yield from state.storage.data.keys()


async def cmd_admin_exit(message: types.Message, state: FSMContext):
    await cmd_start(message, state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state="*")
    dp.register_message_handler(cmd_help, commands=["help"], state="*")
    dp.register_message_handler(grade_chosen, state=UserState.waiting_for_grade)
    dp.register_message_handler(
        cmd_today_schedule, Text(equals=UserCommands.Today.value), state=UserState.grade_defined
    )
    dp.register_message_handler(
        cmd_tomorrow_schedule, Text(equals=UserCommands.Tomorrow.value), state=UserState.grade_defined
    )
    dp.register_message_handler(
        cmd_is_bottom_week, Text(equals=UserCommands.IsBottomWeek.value), state=UserState.grade_defined
    )
    dp.register_message_handler(
        cmd_change_grade, Text(equals=UserCommands.ChangeGrade.value), state=UserState.grade_defined
    )
    # Admin
    dp.register_message_handler(token_passed, Text(equals=bot_token), state="*")
    dp.register_message_handler(
        cmd_broadcast_start, Text(equals=AdminCommands.Broadcast.value), state=UserState.admin_mode_menu
    )
    dp.register_message_handler(cmd_broadcast_send, state=UserState.admin_mode_broadcast_message_waiting)
    dp.register_message_handler(
        cmd_admin_exit, Text(equals=AdminCommands.Exit.value), state=UserState.admin_mode_menu
    )