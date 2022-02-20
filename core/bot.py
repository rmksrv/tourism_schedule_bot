import os

from aiogram import Bot, Dispatcher, types
from loguru import logger

token = os.environ.get("tourism_schedule_bot_token")

if not token:
    logger.error('No bot token defined! Please, pass it to "tourism_schedule_bot_token" env var. Closing...')
    exit()

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dispatcher = Dispatcher(bot)
