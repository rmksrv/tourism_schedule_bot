from datetime import date, timedelta
from pathlib import Path

from telegram import (
    Update,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ParseMode,
)
from telegram.ext import CallbackContext

from core import utils
from core.constants import BotCommands, BOT_NAME, Weekdays
from core.daily_schedule import DailyScheduleParser


def command_handler(update: Update, context: CallbackContext):
    if update.message.text == "/start":
        return start(update, context)
    else:
        return unknown_message(update, context)


def message_handler(update: Update, context: CallbackContext):
    if update.message.text == BotCommands.Today.value:
        return today_schedule(update, context)
    elif update.message.text == BotCommands.Tomorrow.value:
        return tomorrow_schedule(update, context)
    elif update.message.text == BotCommands.IsBottomWeek.value:
        return is_bottom_week(update, context)
    elif update.message.text == BotCommands.ForEnglishSpeaker.value:
        return for_english_speaker(update, context)
    else:
        return unknown_message(update, context)


# Command handlers


def start(update: Update, context: CallbackContext):
    info_message = (
        f"Привет, я бот {BOT_NAME}. Я создан, чтобы потешить эго моего создателя. А еще я могу "
        f"подсказать расписание на сегодня или завтра."
    )
    context.bot.send_message(update.effective_chat.id, info_message)
    action_menu(update, context)


# Message handlers


def action_menu(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BotCommands.Today.value),
                KeyboardButton(text=BotCommands.Tomorrow.value),
            ],
            [
                KeyboardButton(text=BotCommands.IsBottomWeek.value),
                KeyboardButton(text=BotCommands.ForEnglishSpeaker.value),
            ],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text="Выбери действие",
        reply_markup=reply_markup,
    )


def unknown_message(update: Update, context: CallbackContext):
    info_message = "Я это не умею =("
    context.bot.send_message(update.effective_chat.id, info_message)
    action_menu(update, context)


def today_schedule(update: Update, context: CallbackContext):
    d = date.today()
    info_message = f"Расписание на сегодня, <b>{d} ({Weekdays.from_date(d).value})</b>"
    context.bot.send_message(
        update.effective_chat.id, info_message, parse_mode=ParseMode.HTML
    )

    p = DailyScheduleParser(Path("Туризм.docx"))
    grade = 3
    response = utils.beautified_schedule_response(p.today_schedule(grade))
    update.message.reply_text(
        text=response,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
    action_menu(update, context)


def tomorrow_schedule(update: Update, context: CallbackContext):
    d = date.today() + timedelta(days=1)
    info_message = f"Расписание на завтра, <b>{d} ({Weekdays.from_date(d).value})</b>"
    context.bot.send_message(
        update.effective_chat.id, info_message, parse_mode=ParseMode.HTML
    )

    p = DailyScheduleParser(Path("Туризм.docx"))
    grade = 3
    response = utils.beautified_schedule_response(p.tomorrow_schedule(grade))
    update.message.reply_text(
        text=response,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
    action_menu(update, context)


def is_bottom_week(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="<b><i>Да</i></b>" if utils.is_bottom_week() else "<b><i>Неа</i></b>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
    action_menu(update, context)


def for_english_speaker(update, context):
    update.message.reply_text(
        text="I'm sorry very well, how v zhopu do you do? (учите русский)",
        reply_markup=ReplyKeyboardRemove(),
    )
    action_menu(update, context)
